<script lang="ts">
  import Navbar from '$lib/components/Navbar.svelte';
  import Fotter from '$lib/components/Fotter.svelte';
  import '../app.css';
</script>

<div class="flex flex-col min-h-screen">
  <Navbar />

  <main class="flex-1">
    <slot />
  </main>

  <Fotter />
</div>
