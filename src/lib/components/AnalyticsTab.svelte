<script>
  import ComparisonBars from "./ComparisonBars.svelte";
  import HistogramBars from "./HistogramBars.svelte";
  import MetricTile from "./MetricTile.svelte";
  import ResultDisplay from "./ResultDisplay.svelte";
  import { api } from "../api.js";

  export let images = [];

  let selectedImageId = "";
  let analytics = null;
  let loading = false;
  let error = "";

  async function runAnalysis() {
    if (!selectedImageId) return;
    loading = true;
    error = "";
    try {
      analytics = await api.getAnalytics(Number(selectedImageId));
    } catch (analysisError) {
      analytics = null;
      error = analysisError.message;
    } finally {
      loading = false;
    }
  }
</script>

<div class="panel p-6">
  <div class="grid gap-4 md:grid-cols-[1fr_auto]">
    <div>
      <label class="label">Select an image to analyze</label>
      <select class="input" bind:value={selectedImageId}>
        <option value="">Choose image</option>
        {#each images as image}
          <option value={image.image_id}>{image.filename} ({image.uploaded_at})</option>
        {/each}
      </select>
    </div>
    <div class="flex items-end">
      <button class="btn-primary w-full md:w-auto" on:click={runAnalysis} disabled={!selectedImageId || loading}>
        {loading ? "Running..." : "Run Cryptographic Analysis"}
      </button>
    </div>
  </div>
</div>

{#if error}
  <div class="mt-6">
    <ResultDisplay title="Analysis failed" type="error" message={error} />
  </div>
{/if}

{#if analytics}
  <div class="mt-6 space-y-6">
    <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      <MetricTile
        label="Encrypted Entropy"
        value={analytics.entropy.encrypted.toFixed(4)}
        hint="Higher values indicate stronger randomness in encrypted output."
        accent="violet"
      />
      <MetricTile
        label="Randomness Score"
        value={`${analytics.entropy.randomness_score.toFixed(2)}%`}
        hint="Entropy normalized against the 8-bit maximum."
        accent="cyan"
      />
      <MetricTile
        label="Changed Pixel Ratio"
        value={`${(analytics.comparison.changed_pixel_ratio * 100).toFixed(2)}%`}
        hint="Share of flattened pixel values altered by encryption."
        accent="coral"
      />
      <MetricTile
        label="Mean Abs Difference"
        value={analytics.comparison.mean_absolute_difference.toFixed(2)}
        hint="Average distance between original and encrypted intensities."
        accent="emerald"
      />
    </div>

    <div class="grid gap-6 xl:grid-cols-[1.25fr_0.75fr]">
      <HistogramBars
        labels={analytics.histogram.labels}
        original={analytics.histogram.original}
        encrypted={analytics.histogram.encrypted}
      />
      <ComparisonBars comparison={analytics.comparison} />
    </div>

    <div class="grid gap-6 xl:grid-cols-2">
      <ResultDisplay
        title="Entropy Notes"
        type="info"
        message={`Original entropy: ${analytics.entropy.original.toFixed(4)}\nEncrypted entropy: ${analytics.entropy.encrypted.toFixed(4)}\nTarget ceiling: ${analytics.entropy.max.toFixed(1)} bits`}
      />
      <ResultDisplay
        title="Integrity Signature"
        type={analytics.integrity.status === "MATCH" ? "success" : analytics.integrity.status === "FAILED" ? "error" : "warning"}
        message={`Stored hash: ${analytics.integrity.stored_hash || "Not recorded"}\nCalculated hash: ${analytics.integrity.decrypted_hash}\nStatus: ${analytics.integrity.status}`}
      />
    </div>
  </div>
{/if}
