<script>
  export let onGetStarted = () => {};
  export let onLearnMore = () => {};
</script>

<section class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
  <div class="panel relative overflow-hidden px-6 py-16 sm:px-10 lg:px-16">
    <div class="pointer-events-none absolute inset-0 opacity-70">
      <div class="absolute left-[-8rem] top-[-6rem] h-56 w-56 rounded-full bg-violet/20 blur-3xl"></div>
      <div class="absolute right-[-6rem] top-10 h-64 w-64 rounded-full bg-cyan-400/20 blur-3xl"></div>
      <div class="absolute bottom-[-8rem] left-1/2 h-64 w-64 -translate-x-1/2 rounded-full bg-blue-500/10 blur-3xl"></div>
    </div>

    <div class="relative mx-auto max-w-4xl text-center">
      <div class="inline-flex rounded-full border border-white/10 bg-white/10 px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.32em] text-slate-600 dark:text-slate-300">
        Futuristic Secure Imaging
      </div>
      <h1 class="mt-8 font-display text-4xl font-bold tracking-tight sm:text-6xl">
        <span class="bg-gradient-to-r from-violet via-fuchsia-500 to-cyan-400 bg-clip-text text-transparent">
          Hybrid Sine-Wave DNA Encryption
        </span>
      </h1>
      <p class="mx-auto mt-6 max-w-2xl text-base leading-8 text-slate-600 dark:text-slate-300 sm:text-lg">
        Secure image encryption, DNA steganography, integrity proofs, and statistical analytics in one modern full-stack workspace.
      </p>
      <div class="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
        <button class="inline-flex min-w-40 items-center justify-center rounded-2xl bg-gradient-to-r from-cyan-500 to-violet px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-cyan-500/20 transition duration-200 hover:-translate-y-0.5 hover:from-cyan-400 hover:to-fuchsia-500" on:click={onGetStarted}>
          Get Started
        </button>
        <button class="btn-secondary min-w-40" on:click={onLearnMore}>
          Learn More
        </button>
      </div>
    </div>
  </div>

  <section id="features" class="mt-8 grid gap-6 lg:grid-cols-4">
    <div class="soft-card">
      <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-500/10 text-cyan-500">
        <svg viewBox="0 0 24 24" class="h-6 w-6 fill-none stroke-current stroke-[1.8]"><path d="M7 7h10v10H7z"/><path d="M9 9h6v6H9z"/></svg>
      </div>
      <h3 class="font-display text-lg font-semibold text-slate-900 dark:text-slate-100">Image Encryption</h3>
      <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">Lossless image encryption powered by chaos-driven DNA transformations.</p>
    </div>
    <div class="soft-card">
      <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-violet/10 text-violet">
        <svg viewBox="0 0 24 24" class="h-6 w-6 fill-none stroke-current stroke-[1.8]"><path d="M8 3c2 2 2 4 0 6s-2 4 0 6 2 4 0 6"/><path d="M16 3c-2 2-2 4 0 6s2 4 0 6-2 4 0 6"/><path d="M7 6h10"/><path d="M7 18h10"/></svg>
      </div>
      <h3 class="font-display text-lg font-semibold text-slate-900 dark:text-slate-100">DNA Steganography</h3>
      <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">Embed hidden messages directly into DNA-encoded image structure before diffusion.</p>
    </div>
    <div class="soft-card">
      <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-500/10 text-emerald-500">
        <svg viewBox="0 0 24 24" class="h-6 w-6 fill-none stroke-current stroke-[1.8]"><path d="M5 12l4 4L19 6"/><path d="M12 3l7 4v5c0 5-3.5 8-7 9-3.5-1-7-4-7-9V7z"/></svg>
      </div>
      <h3 class="font-display text-lg font-semibold text-slate-900 dark:text-slate-100">Integrity Verification</h3>
      <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">Validate decrypted output against the stored SHA-256 integrity signature.</p>
    </div>
    <div class="soft-card">
      <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-fuchsia-500/10 text-fuchsia-500">
        <svg viewBox="0 0 24 24" class="h-6 w-6 fill-none stroke-current stroke-[1.8]"><path d="M4 18V6"/><path d="M9 18V10"/><path d="M14 18V8"/><path d="M19 18V12"/></svg>
      </div>
      <h3 class="font-display text-lg font-semibold text-slate-900 dark:text-slate-100">Histogram Analysis</h3>
      <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">Inspect diffusion quality with entropy, distribution, and before-vs-after metrics.</p>
    </div>
  </section>

  <section class="mt-8 grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
    <div class="panel p-8">
      <h2 class="font-display text-2xl font-semibold">Built with a modern full-stack workflow</h2>
      <p class="mt-3 text-sm leading-7 text-slate-600 dark:text-slate-300">
        Frontend responsiveness, backend performance, and scientific computing tools come together for an encryption app that feels both rigorous and premium.
      </p>
      <div class="mt-6 flex flex-wrap gap-3">
        <span class="rounded-full border border-cyan-500/20 bg-cyan-500/10 px-4 py-2 text-sm font-medium text-cyan-700 dark:text-cyan-300">Svelte</span>
        <span class="rounded-full border border-violet/20 bg-violet/10 px-4 py-2 text-sm font-medium text-violet-700 dark:text-violet-300">FastAPI</span>
        <span class="rounded-full border border-slate-300/40 bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300">OpenCV</span>
        <span class="rounded-full border border-slate-300/40 bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300">NumPy</span>
      </div>
    </div>

    <div class="panel p-8 text-center">
      <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-3xl bg-gradient-to-br from-cyan-500/20 to-violet/20 text-cyan-500 shadow-lg shadow-cyan-500/10">
        <svg viewBox="0 0 24 24" class="h-8 w-8 fill-none stroke-current stroke-[1.8]"><path d="M12 3a4 4 0 0 0-4 4v2H7a2 2 0 0 0-2 2v7h14v-7a2 2 0 0 0-2-2h-1V7a4 4 0 0 0-4-4Z"/><path d="M10 13h4"/></svg>
      </div>
      <h2 class="mt-5 font-display text-2xl font-semibold">Start Securing Your Images</h2>
      <p class="mt-3 text-sm leading-7 text-slate-600 dark:text-slate-300">
        Jump into the authentication flow and start encrypting, sharing, and verifying images right away.
      </p>
      <button class="mt-6 inline-flex min-w-44 items-center justify-center rounded-2xl bg-gradient-to-r from-cyan-500 to-violet px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-cyan-500/20 transition duration-200 hover:-translate-y-0.5 hover:from-cyan-400 hover:to-fuchsia-500" on:click={onGetStarted}>
        Start Securing Your Images
      </button>
    </div>
  </section>
</section>
