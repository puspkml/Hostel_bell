<script lang="ts">
  import { onMount } from 'svelte';
  let mobileMenuOpen = false;

  function toggleMobileMenu() {
    mobileMenuOpen = !mobileMenuOpen;
  }

  // Close mobile menu if resized to desktop
  onMount(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        mobileMenuOpen = false;
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  });
</script>

<div class="bg-cyan-900 sticky top-0 left-0 w-full h-[70px] flex items-center justify-between px-4 sm:px-6 md:px-8 z-50">
  <!-- Logo -->
  <div class="flex items-center gap-x-2">
    <img src="logo.png" alt="Hostel Logo" class="h-8 w-8" />
    <p class="font-bold text-xl sm:text-2xl text-white">SSSSBH BELL SYSTEM</p>
  </div>

  <!-- Desktop Navigation -->
  <nav class="hidden md:flex ml-auto">
    <ul class="flex flex-row gap-x-6 text-white font-semibold">
      <li><a href="/" class="hover:underline">HOME</a></li>
      <li><a href="/scheduler" class="hover:underline">SCHEDULER</a></li>
      <li><a href="/calendar" class="hover:underline">CALENDAR</a></li>
    </ul>
  </nav>

  <!-- Mobile Hamburger -->
  <div class="md:hidden relative">
    <button class="flex items-center justify-center text-white" on:click={toggleMobileMenu}>
      <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        {#if mobileMenuOpen}
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
        {:else}
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"></path>
        {/if}
      </svg>
    </button>

    <!-- Dropdown Menu -->
    {#if mobileMenuOpen}
      <ul class="absolute right-0 mt-2 w-40 bg-cyan-100 text-black rounded shadow-lg flex flex-col z-50">
        <li>
          <a href="/" class="block px-4 py-2 hover:bg-cyan-100" on:click={() => mobileMenuOpen = false}>HOME</a>
        </li>
        <li>
          <a href="/scheduler" class="block px-4 py-2 hover:bg-cyan-100" on:click={() => mobileMenuOpen = false}>SCHEDULER</a>
        </li>
        <li>
          <a href="/calendar" class="block px-4 py-2 hover:bg-cyan-100" on:click={() => mobileMenuOpen = false}>CALENDAR</a>
        </li>
      </ul>
    {/if}
  </div>
</div>
