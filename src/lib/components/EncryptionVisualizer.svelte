<script>
  import { onDestroy } from "svelte";
  import { getMediaUrl } from "../api.js";

  export let visualization = null;
  export let playing = false;

  let activeIndex = 0;
  let displayUrl = "";
  let timeoutId = null;
  let scrambleSeed = 0;

  $: steps = visualization?.steps || [];
  $: currentStep = steps[activeIndex] || null;

  function clearTimers() {
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
    }
  }

  function runStage(index) {
    if (!steps.length) return;
    activeIndex = index;
    displayUrl = getMediaUrl(steps[index].image_url);
    scrambleSeed += 1;

    if (index >= steps.length - 1) {
      return;
    }

    timeoutId = setTimeout(() => {
      runStage(index + 1);
    }, index === 0 ? 900 : 1200);
  }

  $: if (playing && steps.length) {
    clearTimers();
    runStage(0);
  } else if (!playing && steps.length) {
    clearTimers();
    activeIndex = steps.length - 1;
    displayUrl = getMediaUrl(steps[steps.length - 1].image_url);
  }

  onDestroy(() => {
    clearTimers();
  });
</script>

{#if steps.length}
  <div class="panel p-6">
    <div class="flex flex-col gap-5 lg:flex-row">
      <div class="lg:w-[58%]">
        <div class="relative overflow-hidden rounded-[28px] bg-slate-950">
          <img
            class={`h-[22rem] w-full object-contain transition duration-500 ${playing ? "scale-[1.015]" : ""}`}
            src={displayUrl}
            alt={currentStep?.caption || "Encryption stage"}
          />
          {#if playing}
            <div
              class="pointer-events-none absolute inset-0 opacity-40 mix-blend-screen"
              style={`background:
                linear-gradient(135deg, rgba(255,255,255,0.18), transparent 40%),
                repeating-linear-gradient(
                  ${45 + scrambleSeed * 7}deg,
                  rgba(255,255,255,0.08) 0px,
                  rgba(255,255,255,0.08) 8px,
                  transparent 8px,
                  transparent 18px
                );`}
            ></div>
          {/if}
          <div class="absolute left-4 top-4 rounded-full bg-white/15 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-white backdrop-blur-md">
            {currentStep?.caption}
          </div>
        </div>
      </div>

      <div class="lg:w-[42%]">
        <div class="rounded-[28px] bg-slate-50 p-5 transition-colors duration-300 dark:bg-slate-800/70">
          <div class="text-xs font-semibold uppercase tracking-[0.25em] text-slate-400 dark:text-slate-500">Encryption Visualisation</div>
          <h3 class="mt-3 font-display text-xl font-semibold text-slate-900 dark:text-slate-100">{currentStep?.title}</h3>
          <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">
            {#if currentStep?.id === "original"}
              Loading the source image and preparing plaintext-sensitive hashing.
            {:else if currentStep?.id === "key_preview"}
              Chaotic key matrices are generated from the hyper-chaotic map and prepared for DNA operations.
            {:else if currentStep?.id === "first_diffusion"}
              The first DNA-layer XOR and complement diffusion scramble the visible pixel structure.
            {:else}
              The second diffusion layer completes the encryption and produces the final lossless cipher image.
            {/if}
          </p>

          <div class="mt-5 space-y-3">
            {#each steps as step, index}
              <button
                class={`flex w-full items-center justify-between rounded-2xl border px-4 py-3 text-left transition ${
                  index === activeIndex
                    ? "border-coral bg-coral/10 dark:border-cyan-400/50 dark:bg-cyan-400/10"
                    : "border-slate-200 bg-white hover:border-slate-300 dark:border-slate-700 dark:bg-slate-900/80 dark:hover:border-slate-500"
                }`}
                on:click={() => {
                  clearTimers();
                  activeIndex = index;
                  displayUrl = getMediaUrl(step.image_url);
                }}
              >
                <div>
                  <div class="text-xs uppercase tracking-[0.2em] text-slate-400 dark:text-slate-500">{step.id.replace("_", " ")}</div>
                  <div class="mt-1 text-sm font-semibold text-slate-900 dark:text-slate-100">{step.title}</div>
                </div>
                <div class={`h-3 w-3 rounded-full ${index === activeIndex ? "bg-coral dark:bg-cyan-300" : "bg-slate-200 dark:bg-slate-600"}`}></div>
              </button>
            {/each}
          </div>
        </div>
      </div>
    </div>
  </div>
{/if}
