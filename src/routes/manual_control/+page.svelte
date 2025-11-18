<script>
    import { writable } from "svelte/store";

    let message = writable("");
    let loading = writable(false);
    let disabled = writable(false);

    async function ringBell() {
        loading.set(true);
        disabled.set(true);
        message.set(""); // Clear previous

        try {
            const response = await fetch("/manual_control", {
                method: "POST"
            });
            const result = await response.json();

            if (response.ok) {
                message.set(result.message);
            } else {
                message.set(`Error: ${result.message}`);
            }
        } catch (error) {
            message.set("Error ringing the bell!");
            console.error("Error:", error);
        } finally {
            loading.set(false);
            setTimeout(() => {
                disabled.set(false);
            }, 60000);
        }
    }
</script>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    body {
        margin: 0;
        padding: 0;
        min-height: 100vh;
        background: linear-gradient(135deg, #f8fafc 0%, #e3e6e8 100%);
        font-family: 'Inter', sans-serif;
        color: #273146;
    }
    .center-all {
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background: none;
    }
    .card {
        background: #fff;
        border-radius: 20px;
        padding: 2.5rem 2.25rem 1.5rem 2.25rem;
        box-shadow: 0 8px 32px 0 rgba(32, 35, 38, 0.15);
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 340px;
    }
    .title {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -1.2px;
        margin-bottom: 6px;
        color: #22314b;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #6c7c8b;
        margin-bottom: 0.65rem;
        text-align: center;
    }
    .notice {
        color: #ff6b61;
        font-size: 0.92rem;
        margin-bottom: 1.6rem;
        font-weight: 600;
    }
    .ring-btn {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ff6f61 85%, #ffa18a 100%);
        color: #fff;
        border: none;
        font-size: 2.2rem;
        font-family: inherit;
        font-weight: 700;
        display: flex;
        justify-content: center;
        align-items: center;
        transition:
            transform 0.18s cubic-bezier(.4,2,.6,1),
            box-shadow 0.23s cubic-bezier(.4,2,.6,1),
            background 0.28s;
        box-shadow: 0 4px 20px 0 rgba(250, 89, 75, 0.13);
        cursor: pointer;
        margin-bottom: 1.2rem;
        outline: none;
    }
    .ring-btn:hover:not(:disabled) {
        background: linear-gradient(135deg, #ff3b2f 85%, #ff9f90 100%);
        transform: scale(1.06);
        box-shadow: 0 8px 32px 0 rgba(250, 89, 75, 0.18);
    }
    .ring-btn:disabled {
        background: linear-gradient(135deg, #cfcfcf 80%, #e6e6e6 100%);
        color: #b0b5bb;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }
    .spinner {
        font-size: 2rem;
        color: #fff;
        animation: spin 1s linear infinite;
        margin-right: 0;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg);}
    }
    .message {
        margin-top: 14px;
        font-size: 1rem;
        min-height: 1.2em;
        text-align: center;
    }
    .success-message {
        color: #20b37b;
        font-weight: 600;
    }
    .error-message {
        color: #e34c43;
        font-weight: 600;
    }
</style>

<div class="center-all">
    <div class="card">
        <h1 class="title">Emergency Bell Control</h1>
        <div class="subtitle">
            Press this button to ring the emergency bell instantly.<br>
        </div>
        <div class="notice">
            Note: After ringing, the button will be disabled for 60 seconds to prevent accidental multiple rings.
        </div>

        <button
            class="ring-btn"
            on:click={ringBell}
            disabled={$loading || $disabled}
        >
            {#if $loading}
                <span class="spinner">𖣘</span>
            {:else}
                Ring
            {/if}
        </button>

        <div class="message">
            {#if $message}
                {#if $message.includes("Error")}
                    <span class="error-message">{$message}</span>
                {:else}
                    <span class="success-message">{$message}</span>
                {/if}
            {/if}
        </div>
    </div>
</div>
