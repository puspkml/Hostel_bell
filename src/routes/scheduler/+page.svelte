<script lang="ts">
  import { enhance } from '$app/forms';
  import { invalidateAll } from '$app/navigation';
  import { fly } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  import { onMount } from 'svelte';

  let bellType = 2; // Default to 2 (Normal), since it's now first in the dropdown
  let startDate = '';
  let endDate = '';
  let time = '';
  let selectedDays: string[] = [];

  let form: any;
  let notificationMessage = '';
  let showNotification = false;
  let notificationType: 'success' | 'error' = 'success';
  let loading = true;

  onMount(() => {
    setTimeout(() => {
      loading = false;
    }, 500);
  });

  async function addSchedule(event: Event) {
    const formEl = event.target as HTMLFormElement;
    const data = new FormData(formEl);

    const scheduleName = `Schedule from ${startDate} to ${endDate}`;
    data.append('name', scheduleName);
    data.append('startDate', startDate);
    data.append('endDate', endDate);
    data.append('time', time);
    data.append('bell_type', String(bellType));
    data.append('days', JSON.stringify(selectedDays));

    const response = await fetch(formEl.action, {
      method: 'POST',
      body: data
    });

    const responseData = await response.json();
    form = responseData;
    formEl.reset();

    startDate = '';
    endDate = '';
    time = '';
    bellType = 2; // Reset to default (Normal)
    selectedDays = [];

    notificationMessage = responseData.message || 'Schedule added successfully!';
    notificationType = responseData.success ? 'success' : 'error';
    showNotification = true;

    setTimeout(() => {
      showNotification = false;
      notificationMessage = '';
    }, 3000);

    await invalidateAll();
  }
</script>

<main class="flex items-top justify-center min-h-screen bg-gradient-to-br from-teal-50 to-cyan-100 py-6 sm:py-12 px-4 sm:px-6 lg:px-8">
  <div class="max-w-4xl w-full bg-white rounded-xl shadow-xl overflow-hidden text-base sm:text-lg" transition:fly={{ y: 50, duration: 500, easing: quintOut }}>
    <div class="bg-gradient-to-r from-cyan-600 to-cyan-600 text-white py-4 sm:py-6 lg:py-8 px-4 sm:px-6 lg:px-8">
      <h1 class="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight">Hostel Bell Scheduler</h1>
      <p class="text-sm sm:text-base lg:text-lg text-cyan-200 mt-1 sm:mt-2">Craft your ideal bell schedule with ease and precision.</p>
    </div>

    <div class="p-4 sm:p-6 lg:p-10">
      {#if showNotification}
        <div class="mb-4 sm:mb-6 p-3 sm:p-4 rounded-md shadow-sm border-l-4" 
          class:bg-green-100={notificationType === 'success'}
          class:bg-red-100={notificationType === 'error'}
          class:border-green-500={notificationType === 'success'}
          class:border-red-500={notificationType === 'error'}
          class:text-green-700={notificationType === 'success'}
          class:text-red-700={notificationType === 'error'}
          transition:fly={{ x: 100, duration: 300, easing: quintOut }}>
          <p class="font-bold text-base sm:text-lg lg:text-xl">{notificationType === 'success' ? 'Alert!' : 'Alert!'}</p>
          <p class="text-sm sm:text-base">{notificationMessage}</p>
        </div>
      {/if}

      <div class="max-w-3xl mx-auto bg-white p-4 sm:p-6 rounded-lg shadow-lg">
        <h2 class="text-xl sm:text-2xl font-semibold text-red-800 mb-3 sm:mb-4">📌 INSTRUCTIONS</h2>
        <div class="text-sm sm:text-base text-gray-700 space-y-2 sm:space-y-3">
          <ul class="list-disc pl-6 space-y-1 sm:space-y-2">
            <li><strong>Date Range:</strong> Select the start and end dates for the schedule.</li>
            <li><strong>Time:</strong> Choose the time for bell ringing.</li>
            <li><strong>Days:</strong> Choose the weekdays (Mon-Sun) to repeat the schedule.</li>
            <li><strong>Bell Type:</strong> Select the type of bell: Normal, Supravatam first bell, or Supravatam second bell.</li>
          </ul>
        </div>
      </div>

      <form method="POST" use:enhance on:submit|preventDefault={addSchedule} class="space-y-6 sm:space-y-8 mt-6 sm:mt-0">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
          <div>
            <label class="block text-base sm:text-xl font-medium text-gray-700">Start Date</label>
            <input type="date" bind:value={startDate} class="mt-1 sm:mt-2 p-3 sm:p-4 w-full text-base sm:text-lg border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500" required />
          </div>
          <div>
            <label class="block text-base sm:text-xl font-medium text-gray-700">End Date</label>
            <input type="date" bind:value={endDate} class="mt-1 sm:mt-2 p-3 sm:p-4 w-full text-base sm:text-lg border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500" required />
          </div>
        </div>

        <div>
          <label class="block text-base sm:text-xl font-medium text-gray-700">Time</label>
          <input type="time" bind:value={time} class="mt-1 sm:mt-2 p-3 sm:p-4 w-full text-base sm:text-lg border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500" required />
        </div>

        <div>
          <label class="block text-base sm:text-xl font-medium text-gray-700 mb-2">Days of the Week</label>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-3 text-sm sm:text-base">
            {#each [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday'] as day, index}
              <label class="flex items-center p-2 cursor-pointer rounded border border-gray-200 hover:bg-gray-50">
                <input type="checkbox" bind:group={selectedDays} value={index.toString()} class="mr-2 h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
                <span class="text-xs sm:text-sm">{day}</span>
              </label>
            {/each}
          </div>
        </div>

        <div>
          <label class="block text-base sm:text-xl font-medium text-gray-700">Bell Type</label>
          <select bind:value={bellType} class="mt-1 sm:mt-2 p-3 sm:p-4 w-full text-base sm:text-lg border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500" required>
            <option value={2}>Normal</option>
            <option value={0}>Supravatam first bell</option>
            <option value={1}>Supravatam second bell</option>
          </select>
        </div>

        <div>
          <button type="submit" class="w-full py-3 sm:py-4 px-4 sm:px-6 text-base sm:text-lg font-medium text-white bg-cyan-600 hover:bg-cyan-700 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 transition-all duration-200">
            Add Schedule
          </button>
        </div>
      </form>
    </div>
  </div>
</main>