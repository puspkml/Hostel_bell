<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { formatScheduleDate } from '$lib/utils/date';

	export let data: {
		error?: string;
		schedules: any[];
		sortKey?: string;
		sortOrder?: string;
	};

	let loading = false;
	let deletingId: number | null = null;
	let showConfirmation = false;
	let scheduleToDelete: any = null;
	let searchQuery = '';

	// Function to get bell type name
	function getBellTypeName(bellType: number): string {
		switch (bellType) {
			case 0:
				return 'Supravatam first bell';
			case 1:
				return 'Supravatam second bell';
			case 2:
				return 'Normal';
			default:
				return 'Unknown';
		}
	}

	// ✅ Filter directly on `data.schedules`
	$: filteredSchedules = (data.schedules || []).filter((s) => {
		const formatted = formatScheduleDate(s.schedule_date, s.schedule_time);

		// Build a combined string: raw + formatted + bell type name
		const searchString = `
			${s.schedule_date}
			${s.schedule_time}
			${formatted.date}
			${formatted.time}
			${getBellTypeName(s.bell_type).toLowerCase()}
			${s.name || ''}
		`.toLowerCase();

		return searchString.includes(searchQuery.toLowerCase());
	});


	function confirmDelete(schedule: any) {
		scheduleToDelete = schedule;
		showConfirmation = true;
	}

	function cancelDelete() {
		showConfirmation = false;
		scheduleToDelete = null;
	}
	function PastBells() {
		goto('/past_bells');
	}

	
</script>

<svelte:head>
	<title>SCHEDULES</title>
</svelte:head>
<main class="flex items-top justify-center min-h-screen bg-gradient-to-br from-teal-50 to-cyan-100 py-12 px-4 sm:px-6 lg:px-8">

	<div class="container">
		<div class="header-bar">
				<h1>SCHEDULES</h1>
				<button class="nav-button" on:click={PastBells}>Past Bells</button>
		</div>
		<h2 class="refresh-message">
		Note: After the delete operation kindly refresh the page.</h2>


		<div class="search-container">
			<input type="text" placeholder="Search schedules..." bind:value={searchQuery} />
		</div>

		{#if data.error}
			<div class="error-message" transition:fly={{ y: -20, duration: 200, easing: quintOut }}>
				{data.error}
			</div>
		{:else if !data.schedules || data.schedules.length === 0}
			<div class="empty-state" transition:fly={{ y: -20, duration: 200, easing: quintOut }}>
				<p>No schedules found. Create one to get started!</p>
			</div>
		{:else}
			<div class="table-wrapper">
				<table>
					<thead>
						<tr>
							<th>Date</th>
							<th>Time</th>
							<th>Bell Type</th>
							<th>Actions</th>
						</tr>
					</thead>
					<tbody>
						{#each filteredSchedules as schedule (schedule.id)}
							<tr transition:fly={{ y: 20, duration: 200, easing: quintOut }}>
								<td>{formatScheduleDate(schedule.schedule_date, schedule.schedule_time).date}</td>
								<td>{formatScheduleDate(schedule.schedule_date, schedule.schedule_time).time}</td>
								<td class="bell-type-cell">
									<span class="bell-type-indicator">{getBellTypeName(schedule.bell_type)}</span>
								</td>
								<td>
									<button
										class="delete-button"
										on:click={() => confirmDelete(schedule)}
										disabled={deletingId === schedule.id}
									>
										{deletingId === schedule.id ? 'Deleting...' : 'Delete'}
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}

		{#if showConfirmation && scheduleToDelete}
			<div class="confirmation-overlay">
				<div class="confirmation-dialog">
						<p>
						Are you sure you want to delete the schedule on 
						<strong>{scheduleToDelete.schedule_date}</strong> at 
						<strong>{scheduleToDelete.schedule_time}</strong>?
						</p>				<div class="confirmation-buttons">
						<button class="cancel-button" on:click={cancelDelete}>Cancel</button>

						<form
							method="POST"
							action="?/deleteSchedule"
							use:enhance={({ update }) => {
								return async ({ result }) => {
									loading = true;
									deletingId = scheduleToDelete.id;

									// ✅ Optimistic removal
									filteredSchedules = filteredSchedules.filter(
										(s) => s.id !== scheduleToDelete.id
									);

									if (result.type === 'success') {
										// ✅ Force re-fetch schedules from Flask (server-side load)
										await update();
									}

									loading = false;
									deletingId = null;
									showConfirmation = false;
									scheduleToDelete = null;
								};
							}}
						>
							<input type="hidden" name="scheduleId" value={scheduleToDelete.id} />
							<button type="submit" class="confirm-delete-button">
								Confirm Delete
							</button>
						</form>

		



					</div>
				</div>
			</div>
		{/if}

		{#if loading}
			<div class="loading-overlay">
				<div class="spinner"></div>
			</div>
		{/if}
	</div>
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
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
		max-width: 900px;
		margin: 20px auto;
	}

	.header-bar {
		display: flex;
		justify-content: space-between;
		align-items: center;
		flex-wrap: wrap;
		margin-bottom: 15px;
	}

	.nav-buttons {
		display: flex;
		gap: 10px;
	}

	.nav-button {
		padding: 8px 16px;
		background-color: var(--accent-color);
		color: var(--background-color);
		border: none;
		border-radius: 5px;
		cursor: pointer;
		transition: background-color 0.2s ease-in-out;
	}

	.nav-button:hover {
		background-color: #3d8275;
	}

	h1 {
		color: var(--primary-color);
		text-align: center;
		margin-bottom: 20px;
		font-weight: 500;
	}

	.refresh-message {
		text-align: center;
		color: rgb(197, 155, 63);
		font-style: italic;
		font-weight: bold;
		margin-top: 10px;
	}

	.search-container {
		margin: 20px 0;
		display: flex;
		gap: 10px;
	}

	.search-container input {
		flex: 1;
		padding: 10px;
		border-radius: 4px;
		border: 1px solid #ccc;
		background-color: var(--background-color);
		color: var(--text-color);
	}

	.search-container input::placeholder {
		color: #999;
	}

	.search-button {
		background-color: var(--accent-color);
		color: var(--background-color);
		padding: 10px 16px;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		transition: background-color 0.2s;
	}

	.search-button:hover {
		background-color: #3d8275;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		margin-bottom: 20px;
		background-color: #1e2d48;
		border-radius: 6px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	th, td {
		border: 1px solid #33435b;
		padding: 12px 15px;
		text-align: left;
	}

	th {
		background-color: var(--accent-color);
		color: var(--background-color);
		font-weight: 600;
		text-transform: uppercase;
	}

	tbody tr:nth-child(even) {
		background-color: #283d5b;
	}

	.delete-button, .confirm-delete-button, .cancel-button {
		padding: 8px 16px;
		border-radius: 5px;
		border: none;
		cursor: pointer;
		transition: background-color 0.2s ease-in-out;
	}

	.delete-button {
		background-color: #e53935;
		color: white;
	}

	.delete-button:hover {
		background-color: #c62828;
	}

	.delete-button:disabled {
		background-color: gray;
		cursor: not-allowed;
	}

	.confirm-delete-button {
		background-color: var(--error-color);
		color: white;
	}

	.confirm-delete-button:hover {
		background-color: #d32f2f;
	}

	.cancel-button {
		background-color: #607d8b;
		color: white;
	}

	.cancel-button:hover {
		background-color: #455a64;
	}

	.confirmation-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 10;
	}

	.confirmation-dialog {
		background-color: var(--background-color);
		padding: 20px;
		border-radius: 8px;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
		text-align: center;
		width: 80%;
		max-width: 500px;
	}

	.confirmation-buttons {
		display: flex;
		justify-content: space-around;
		margin-top: 20px;
	}

	.loading-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 100;
	}

	.spinner {
		border: 4px solid rgba(255, 255, 255, 0.3);
		border-top: 4px solid var(--primary-color, #4f46e5);
		border-radius: 50%;
		width: 50px;
		height: 50px;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
</style>
