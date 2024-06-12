<script>
	import 'bootstrap/dist/css/bootstrap.min.css';

	import { onMount } from 'svelte';

	let showAlert = false;

	function setAlertSetting() {
		showAlert = false;
		localStorage.setItem('showAlert', showAlert ? '' : 'no');
	}

	onMount(() => {
		const value = localStorage.getItem('showAlert');
		if (value === 'no') showAlert = false;
		else showAlert = true;
	});
</script>

<div class="d-flex flex-column w-100">
	<div class="alert alert-warning alert-dismissible fade w-100" role="alert" class:show={showAlert}>
		The prediction will be slow at the first time due to waking up the service
		<button type="button" class="btn-close" aria-label="Close" on:click={setAlertSetting}></button>
	</div>
	<slot />
</div>
