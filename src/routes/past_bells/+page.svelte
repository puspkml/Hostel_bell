<script lang="ts">
	import { goto } from '$app/navigation';

	export let data: {
		logs: {
			id: number;
			bell_type: number;
			date_logged: string;
			ring_time: string;
		}[];
	};

	let searchDate = '';

	function getBellTypeName(bellType: number) {
		switch (bellType) {
			case 0: return 'Supravatam First Bell';
			case 1: return 'Supravatam Second Bell';
			case 2: return 'Normal';
			default: return 'Unknown';
		}
	}

	function filteredLogs() {
		if (!searchDate) return data.logs;
		return data.logs.filter(log => log.date_logged.includes(searchDate));
	}

	function goToFutureBells() {
		goto('/calendar'); // adjust path if needed
	}
</script>

<main class="container">
	<div class="header-bar">
		<h1>Bell Log History</h1>
		<button class="nav-button" on:click={goToFutureBells}>View Future Scheduled Bells</button>
	</div>

	

	{#if !filteredLogs() || filteredLogs().length === 0}
		<p class="empty-state">No bells found for this date.</p>
	{:else}
		<div class="table-wrapper">
			<table>
				<thead>
					<tr>
						<th>Bell Type</th>
						<th>Date</th>
						<th>Time</th>
					</tr>
				</thead>
				<tbody>
					{#each filteredLogs() as log}
						<tr>
							<td>{getBellTypeName(log.bell_type)}</td>
							<td>{log.date_logged}</td>
							<td>{log.ring_time}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</main>

<style>
	:root {
		--primary-color: #64ffda;
		--background-color: #0a192f;
		--text-color: #ccd6f6;
		--accent-color: #499585;
		--error-color: #f44336;
	}

	.container {
		font-family: "Roboto", sans-serif;
		color: var(--text-color);
		background-color: var(--background-color);
		padding: 20px;
		border-radius: 8px;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
		max-width: 850px;
		margin: 40px auto;
	}

	.header-bar {
		display: flex;
		justify-content: space-between;
		align-items: center;
		flex-wrap: wrap;
		margin-bottom: 15px;
	}

	h1 {
		color: var(--primary-color);
		font-size: 1.8rem;
		font-weight: 500;
		margin: 0;
	}

	.nav-button {
		background-color: var(--accent-color);
		color: var(--background-color);
		border: none;
		padding: 10px 18px;
		border-radius: 6px;
		cursor: pointer;
		font-weight: 500;
		transition: all 0.2s ease-in-out;
	}

	.nav-button:hover {
		background-color: #3d8376;
	}

	.search-container {
		margin: 15px 0 25px 0;
		display: flex;
		justify-content: center;
	}

	.search-input {
		padding: 10px 14px;
		border-radius: 6px;
		border: 1px solid #33435b;
		background-color: #112240;
		color: var(--text-color);
		width: 60%;
		text-align: center;
		font-size: 1rem;
	}

	.search-input::placeholder {
		color: #8892b0;
	}

	.empty-state {
		padding: 12px;
		border-radius: 6px;
		border: 1px dashed var(--accent-color);
		color: var(--text-color);
		background-color: rgba(73, 149, 133, 0.1);
		text-align: center;
	}

	.table-wrapper {
		overflow-x: auto;
		border-radius: 8px;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		background-color: #112240;
		border-radius: 8px;
		overflow: hidden;
	}

	th, td {
		padding: 12px 16px;
		text-align: left;
		border-bottom: 1px solid #233554;
	}

	th {
		background-color: var(--accent-color);
		color: var(--background-color);
		font-weight: 600;
		text-transform: uppercase;
		font-size: 0.9rem;
	}

	td {
		color: var(--text-color);
		font-size: 0.95rem;
	}

	tbody tr:nth-child(even) {
		background-color: #1b2b46;
	}

	tbody tr:hover {
		background-color: #233554;
		transition: background-color 0.2s ease-in-out;
	}
</style>
