<script>
  import { onMount } from 'svelte';
  import { sineInOut } from 'svelte/easing';
  import { fly, fade } from 'svelte/transition';

  let loading = true;
  let currentImage = 0;
  /**
   * @type {string | number | NodeJS.Timeout | undefined}
   */
  let intervalId;

  // Image array
  const images = ['/image.png', '/image2.png', '/image3.png'];

  const goToCalendarPage = () => {
    window.location.href = '/calendar';
  };

  const goToSchedulerPage = () => {
    window.location.href = '/scheduler';
  };

  const gotoManualPage = () => {
    window.location.href = '/manual_control';
  };
  const gotoAboutPage = () => {
    window.location.href = '/About';
  };

  onMount(() => {
    // Simulate loading time
    setTimeout(() => {
      loading = false;
    }, 500);

    // Image rotator timing
    intervalId = setInterval(() => {
      currentImage = (currentImage + 1) % images.length;
    }, 5000); // Change image every 5 seconds

    return () => clearInterval(intervalId); // Clear interval on unmount
  });

 
</script>



<div class="min-h-screen flex flex-col">
  <!-- Header -->

  <!-- Main Content (Hero Section) -->
  <main
    class="relative bg-cyan-800 flex-grow text-white flex flex-col justify-center items-center py-0 overflow-hidden"
  >
    <!-- Image Background -->
    {#key currentImage}
      <!-- svelte-ignore element_invalid_self_closing_tag -->
      <div
        class="absolute top-0 left-0 w-full h-full image-background"
        style="background: url({images[currentImage]}); background-size: cover; background-position: center; filter: brightness(0.5);"
        transition:fade={{ duration: 1000 }}
        
      />
    {/key}

    <div class="relative z-10 text-center">
      <h1 class="text-5xl font-bold mb-4">SRI SATHYA SAI HOSTEL BELL SYSTEM</h1>
      <h2 class="text-3xl mb-2">for</h2>
      <h1 class="text-5xl font-bold mb-4">SENIOR BOYS</h1>
      <p class="text-xl italic">"Home Away From Home"</p>
      <p class="italic mb-2">A place where one lives for the other and all live for God.</p>
    </div>
  </main>

  <!-- Features Section -->
  <div class="flex justify-center items-center h-400">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Calendar -->
      <div
        class="feature-card bg-white p-5 rounded-2xl shadow-md hover:shadow-lg transition-shadow duration-300 transform hover:-translate-y-1"
      >
        <!-- svelte-ignore element_invalid_self_closing_tag -->
        <i class="fas fa-calendar-alt text-4xl text-teal-600 mb-3" aria-hidden="true" />
        <h3 class="text-xl font-semibold text-gray-800 mb-2">View Schedule</h3>
        <p class="text-gray-600">Access the daily bell schedule in a clear formatted table.</p>
        <button class="btn-primary mt-4" on:click={goToCalendarPage}>View Calendar</button>
      </div>

      <!-- Scheduler -->
      <div
        class="feature-card bg-white p-5 rounded-2xl shadow-md hover:shadow-lg transition-shadow duration-300 transform hover:-translate-y-1"
      >
        <!-- svelte-ignore element_invalid_self_closing_tag -->
        <i class="fas fa-clock text-4xl text-teal-600 mb-3" aria-hidden="true" />
        <h3 class="text-xl font-semibold text-gray-800 mb-2">Customize Schedule</h3>
        <p class="text-gray-600">Modifications to bell timings through the scheduler.</p>
        <button class="btn-primary mt-4" on:click={goToSchedulerPage}>Go to Scheduler</button>
      </div>

      <!-- Manual Control -->
      <div
        class="feature-card bg-white p-5 rounded-2xl shadow-md hover:shadow-lg transition-shadow duration-300 transform hover:-translate-y-1"
      >
        <!-- svelte-ignore element_invalid_self_closing_tag -->
        <i class="fas fa-bell text-4xl text-teal-600 mb-3" aria-hidden="true" />
        <h3 class="text-xl font-semibold text-gray-800 mb-2">Manual Control</h3>
        <p class="text-gray-600">Emergency bell ringing or unscheduled adjustments.</p>
        <button class="btn-primary mt-4" on:click={gotoManualPage}>Manual Control</button>
      </div>

      <!-- About -->
      <div
        class="feature-card bg-white p-5 rounded-2xl shadow-md hover:shadow-lg transition-shadow duration-300 transform hover:-translate-y-1"
      >
        <!-- svelte-ignore element_invalid_self_closing_tag -->
        <i class="fas fa-info-circle text-4xl text-teal-600 mb-3" aria-hidden="true" />
        <h3 class="text-xl font-semibold text-gray-800 mb-2">About</h3>
        <p class="text-gray-600">Learn about the Bell System's purpose and development.</p>
        <button class="btn-primary mt-4" on:click={gotoAboutPage}>Learn More</button>
      </div>
    </div>
  </div>

  <!-- Footer -->
  
</div>

<style>
  /* Import Font Awesome CSS */
  @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

  /* General Styles */
  body {
    margin: 0;
    font-family: 'Roboto', sans-serif;
    background-color: #f9f9f9;
    color: #333;
  }

  html,
  body {
    touch-action: pan-y;
    overscroll-behavior-y: contain;
  }

  section {
    background: linear-gradient(to bottom, #dff9ef, #e8f5e9); /* Softer background */
    transition: filter 0.3s ease;
  }

  section.blur {
    filter: blur(5px);
  }

  h1,
  h2,
  h3 {
    font-family: 'Poppins', sans-serif; /* A slightly more playful heading font */
    font-weight: 600;
  }

  /* Hero Section */
  .relative {
    position: relative;
  }

  /* Feature Cards */
  .feature-card {
    display: flex;
    flex-direction: column;
    align-items: flex-start; /* Align items to the start */
    justify-content: flex-start; /* Add this line */
    height: 100%; /* Ensure cards take up full height */
  }

  /* Primary Button Style */
  .btn-primary {
    @apply px-4 py-2 bg-cyan-800 text-white rounded-full hover:bg-cyan-600 transition-colors
      duration-200 block w-full text-center font-bold; /* Rounded buttons, bolder font */
  }



  /* Media Query for Smaller Screens */
  @media (max-width: 768px) {
    /* Adjust zoom level and speed for mobile */
    @keyframes zoomInOut {
      0% {
        transform: scale(1);
      }
      100% {
        transform: scale(1.1); /* Reduced zoom on mobile */
      }
    }

    .image-background.zoomed-in {
      animation: zoomInOut 12s linear infinite alternate; /* Slower zoom on mobile */
    }

    /* Mobile-specific styles */
    .grid {
      grid-template-columns: 1fr; /* Stack items vertically */
    }

    .feature-card {
      padding: 1.5rem;
    }

    .feature-card h3 {
      font-size: 1.2rem;
    }

    .feature-card p {
      font-size: 0.9rem;
    }
    .h-400 {
        height: auto; /* Allow content to determine height on smaller screens */
    }
  }
</style>
