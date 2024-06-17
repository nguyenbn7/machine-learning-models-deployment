<script>
	import { PUBLIC_BASE_API } from '$env/static/public';
	import startCase from 'lodash/startCase';

	let tabIndex = 0;
	let errorMessage = '';
	/**
	 * @type {HTMLInputElement}
	 */
	let inputFileNode;
	/**
	 * @type {HTMLImageElement}
	 */
	let previewImageNode;
	/**
	 * @type {File}
	 */
	let dogImage;
	let dogBreed = '';
	let bestScore = '';
	/**
	 * @type { {[x: string]: number} }
	 */
	let top5Scores;
	let isPredicting = false;

	/**
	 * @param {string} url
	 */
	function isImageURL(url) {
		return url.match(/\.(jpeg|jpg|gif|png)$/) != null;
	}

	/**
	 * @param {File} imageFile
	 */
	function showImageToPreviewSection(imageFile) {
		const fileReader = new FileReader();

		previewImageNode.title = imageFile.name;

		fileReader.onload = (ev) => {
			const target = ev.target;
			if (!target || !target.result) return;
			previewImageNode.src = target.result.toString();
		};

		fileReader.readAsDataURL(imageFile);
	}

	/**
	 * @param {Event & { currentTarget: EventTarget & HTMLInputElement }} $event
	 */
	function onImageSelected($event) {
		const imageFiles = $event.currentTarget.files;
		if (!imageFiles) return;

		dogImage = imageFiles[0];
		showImageToPreviewSection(dogImage);
	}

	/**
	 * @param {Event & { currentTarget: EventTarget & HTMLInputElement; }} $event
	 */
	async function handleImageUrl($event) {
		if (!isImageURL($event.currentTarget.value)) {
			errorMessage = 'Invalid Url';
			return;
		}

		const imageUrl = $event.currentTarget.value;
		const response = await fetch(imageUrl);
		const imageContent = await response.blob();

		const imageName = imageUrl.split('/').pop() ?? '';
		dogImage = new File([imageContent], imageName);

		showImageToPreviewSection(dogImage);
	}

	async function predict() {
		try {
			if (!dogImage) return;

			const imageData = new FormData();
			imageData.append('image_file', dogImage);

			isPredicting = true;
			dogBreed = '';
			bestScore = '';
			top5Scores = {};

			const response = await fetch(`${PUBLIC_BASE_API}/classification/dog-breeds`, {
				method: 'POST',
				body: imageData
			});

			const data = await response.json();

			dogBreed = startCase(data['breed']);
			bestScore = `${data['best confidence']}`;
			top5Scores = Object.assign(data['top 5'], {});
		} catch (error) {
			console.log(error);
			// @ts-ignore
			dogBreed = error;
		} finally {
			isPredicting = false;
		}
	}
</script>

<svelte:head>
	<title>Machine Learning Demo - Dog Breeds Classification</title>
</svelte:head>

<div class="cover-container d-flex w-100 px-3 pb-4 flex-column mx-auto flex-grow-1">
	<h1 class="mb-3">Dog Breeds Classification</h1>
	<p class="lead">
		<span class="text-info fw-bold">NOTE: </span>
		<span class="fst-italic">
			If you upload an image not a dog, machine can not detect it correctly
		</span>
	</p>

	<main class="w-100 h-100 mt-3 row">
		<div class="col-8">
			<ul class="nav nav-tabs mb-1">
				{#each Array(2) as _, idx}
					<li class="nav-item">
						<a
							class="nav-link"
							href={'#'}
							class:active={tabIndex === idx}
							on:click={() => {
								tabIndex = idx;
								dogBreed = '';
								bestScore = '';
								top5Scores = {};
							}}
						>
							{#if idx === 0}
								File
							{:else if idx === 1}
								Link
							{/if}
						</a>
					</li>
				{/each}
			</ul>
			{#if tabIndex === 1}
				<div class="mt-2 mb-1 input-group">
					<input
						type="text"
						name="Image URL"
						class="form-control me-1"
						placeholder="https://example.com/dog_image.(jpg | png)"
						on:input={handleImageUrl}
						disabled={isPredicting}
					/>
					<button
						class="btn btn-primary px-4 p-2"
						disabled={!previewImageNode?.src || isPredicting}
						on:click={predict}
					>
						Detect
						{#if isPredicting}
							<span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
						{/if}
					</button>
				</div>
				<div class="w-100 h-75 position-relative mt-2">
					{#if !previewImageNode?.src}
						<div
							class="border border-white border-opacity-50 rounded border-2 h-100"
							style="--bs-border-style: dashed;"
						></div>
						<p class="position-absolute top-50 start-50 translate-middle">
							{#if errorMessage}
								{errorMessage}
							{:else}
								{'Preview your image'}
							{/if}
						</p>
					{/if}
					<!-- svelte-ignore a11y-missing-attribute -->
					<img class="img-fluid" bind:this={previewImageNode} />
				</div>
			{:else if tabIndex === 0}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<div class="w-100 h-75 position-relative mt-2">
					<input
						type="file"
						name="file"
						accept="image/png, image/jpeg"
						style="display: none;"
						bind:this={inputFileNode}
						on:change={onImageSelected}
					/>
					{#if !previewImageNode || !previewImageNode.src}
						<div
							class="border border-white w-100 h-100 border-opacity-50 rounded border-2"
							style="--bs-border-style: dashed; cursor: pointer;"
							on:click={() => inputFileNode.click()}
						></div>
						<p class="position-absolute top-50 start-50 translate-middle">
							<i class="fa-solid fa-upload me-2"></i> Upload your image
						</p>
					{:else}
						<button
							class="btn btn-primary p-2 w-100 mb-4"
							on:click={predict}
							disabled={isPredicting}
						>
							Detect
							{#if isPredicting}
								<span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
							{/if}
						</button>
					{/if}
					<!-- svelte-ignore a11y-missing-attribute -->
					<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
					<img
						class="img-fluid"
						bind:this={previewImageNode}
						on:click={() => inputFileNode.click()}
						style="cursor: pointer;"
					/>
				</div>
			{/if}
		</div>

		<div class="col-4 p-0">
			<table class="mb-3 w-100">
				<tbody>
					<tr>
						<th scope="row" class="text-start">
							<span class="text-success fw-bold">Best match:</span>
						</th>
						<td class="text-end">
							<a
								href="https://en.wikipedia.org/wiki/{dogBreed.replace(/\s+/g, '_')}"
								class="text-white text-decoration-none"
							>
								{dogBreed}
							</a>
						</td>
					</tr>
					<tr>
						<th scope="row" class="text-start">
							<span class="text-info">Confidence score:</span>
						</th>
						<td class="text-end">{bestScore}</td>
					</tr>
				</tbody>
			</table>

			<table class="table table-hover table-dark table-sm caption-top">
				<caption class="text-white fw-semibold">Top 5 predictions</caption>
				<thead>
					<tr>
						<th scope="col">#</th>
						<th scope="col">Breed</th>
						<th scope="col">Confidence</th>
					</tr>
				</thead>
				<tbody>
					{#if top5Scores}
						{#each Object.entries(top5Scores) as [key, value], idx}
							<!-- content here -->
							{@const breedName = startCase(key)}
							<tr>
								<th scope="row">{idx + 1}</th>
								<td
									><a
										href="https://en.wikipedia.org/wiki/{breedName.replace(/\s+/g, '_')}"
										class="text-white text-decoration-none"
									>
										{breedName}
									</a>
								</td>
								<td>{`${value}`}</td>
							</tr>
						{/each}
					{/if}
				</tbody>
			</table>
			<!-- <div class="border border-white h-75"></div> -->
		</div>
	</main>
</div>

<style>
	.cover-container {
		max-width: 70em;
	}
</style>
