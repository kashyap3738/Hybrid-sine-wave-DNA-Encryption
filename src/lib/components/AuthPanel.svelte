<script>
  import { createEventDispatcher } from "svelte";

  export let loading = false;
  export let error = "";
  export let registerError = "";
  export let registerSuccess = "";
  export let initialMode = "login";
  export let onBack = () => {};

  const dispatch = createEventDispatcher();

  let username = "";
  let password = "";
  let regUsername = "";
  let regPassword = "";
  let confirmPassword = "";
  let mode = initialMode;
  let lastInitialMode = initialMode;
  let localError = "";

  $: if (initialMode !== lastInitialMode) {
    mode = initialMode;
    lastInitialMode = initialMode;
  }

  $: passwordChecks = {
    length: regPassword.length >= 8,
    lowercase: /[a-z]/.test(regPassword),
    uppercase: /[A-Z]/.test(regPassword),
    number: /[0-9]/.test(regPassword)
  };

  function submitLogin() {
    localError = "";
    dispatch("login", { username, password });
  }

  function submitRegister() {
    localError = "";
    if (regPassword !== confirmPassword) {
      localError = "Passwords do not match.";
      return;
    }
    dispatch("register", { username: regUsername, password: regPassword });
  }
</script>

<section class="flex min-h-screen items-center justify-center px-4 py-10 sm:px-6">
  <div class="panel w-full max-w-md animate-[fadeIn_220ms_ease-out] rounded-[32px] p-8 sm:p-10">
    <div class="text-center">
      <button class="mx-auto inline-flex items-center gap-2 text-sm font-medium text-slate-500 transition hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100" on:click={onBack}>
        <span aria-hidden="true">←</span>
        <span>Back to landing</span>
      </button>
      <div class="mx-auto flex h-20 w-20 items-center justify-center rounded-[28px] bg-gradient-to-br from-cyan-500/20 to-violet/20 text-cyan-500 shadow-[0_0_40px_rgba(34,211,238,0.22)] dark:text-cyan-300">
        <svg viewBox="0 0 24 24" class="h-10 w-10 fill-none stroke-current stroke-[1.7]">
          <path d="M8 3c2 2 2 4 0 6s-2 4 0 6 2 4 0 6"/>
          <path d="M16 3c-2 2-2 4 0 6s2 4 0 6-2 4 0 6"/>
          <path d="M7 6h10"/>
          <path d="M7 18h10"/>
        </svg>
      </div>
      <div class="mt-5 inline-flex rounded-full bg-gradient-to-r from-cyan-500/15 to-violet/15 px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.28em] text-cyan-700 dark:text-cyan-300">
        Hybrid Sine-Wave DNA Encryption
      </div>
      <h1 class="mt-5 font-display text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
        {mode === "login" ? "Authentication" : "Create your account"}
      </h1>
      <p class="mt-2 text-sm text-slate-500 dark:text-slate-400">
        Secure peer-to-peer image protection with DNA-chaos encryption.
      </p>
    </div>

    <div class="mt-6 grid grid-cols-2 rounded-2xl border border-slate-200 bg-slate-100 p-1 dark:border-slate-700 dark:bg-slate-800">
      <button class={`rounded-xl px-4 py-2 text-sm font-semibold transition ${mode === "login" ? "bg-white text-slate-900 shadow-sm dark:bg-slate-950 dark:text-slate-100" : "text-slate-500 dark:text-slate-400"}`} on:click={() => { mode = "login"; localError = ""; }}>
        Login
      </button>
      <button class={`rounded-xl px-4 py-2 text-sm font-semibold transition ${mode === "register" ? "bg-white text-slate-900 shadow-sm dark:bg-slate-950 dark:text-slate-100" : "text-slate-500 dark:text-slate-400"}`} on:click={() => { mode = "register"; localError = ""; }}>
        Register
      </button>
    </div>

    {#if localError}
      <div class="mt-6 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-900 dark:border-rose-500/30 dark:bg-rose-500/10 dark:text-rose-200">
        {localError}
      </div>
    {/if}

    {#if mode === "login" && error}
      <div class="mt-6 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-900 dark:border-rose-500/30 dark:bg-rose-500/10 dark:text-rose-200">
        {error}
      </div>
    {/if}
    {#if mode === "register" && registerError}
      <div class="mt-6 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-900 dark:border-rose-500/30 dark:bg-rose-500/10 dark:text-rose-200">
        {registerError}
      </div>
    {/if}
    {#if mode === "register" && registerSuccess}
      <div class="mt-6 rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-900 dark:border-emerald-500/30 dark:bg-emerald-500/10 dark:text-emerald-200">
        {registerSuccess}
      </div>
    {/if}

    {#if mode === "login"}
      <div class="mt-6 space-y-4">
        <div>
          <label class="label">Username</label>
          <input class="input" bind:value={username} />
        </div>
        <div>
          <label class="label">Password</label>
          <input class="input" type="password" bind:value={password} />
        </div>
        <button class="inline-flex w-full items-center justify-center rounded-2xl bg-gradient-to-r from-cyan-500 to-violet px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-cyan-500/20 transition duration-200 hover:-translate-y-0.5 hover:from-cyan-400 hover:to-fuchsia-500" on:click={submitLogin} disabled={loading}>
          {loading ? "Signing in..." : "Sign in"}
        </button>
      </div>
    {:else}
      <div class="mt-6 space-y-4">
        <div>
          <label class="label">Username</label>
          <input class="input" bind:value={regUsername} />
        </div>
        <div>
          <label class="label">Password</label>
          <input class="input" type="password" bind:value={regPassword} />
        </div>
        <div>
          <label class="label">Confirm password</label>
          <input class="input" type="password" bind:value={confirmPassword} />
        </div>

        <div class="space-y-2 rounded-3xl bg-slate-50 p-4 text-sm dark:bg-slate-800/70">
          <div class={passwordChecks.length ? "text-emerald-600 dark:text-emerald-300" : "text-rose-500 dark:text-rose-300"}>{passwordChecks.length ? "OK" : "X"} Minimum 8 characters</div>
          <div class={passwordChecks.lowercase ? "text-emerald-600 dark:text-emerald-300" : "text-rose-500 dark:text-rose-300"}>{passwordChecks.lowercase ? "OK" : "X"} At least one lowercase letter</div>
          <div class={passwordChecks.uppercase ? "text-emerald-600 dark:text-emerald-300" : "text-rose-500 dark:text-rose-300"}>{passwordChecks.uppercase ? "OK" : "X"} At least one uppercase letter</div>
          <div class={passwordChecks.number ? "text-emerald-600 dark:text-emerald-300" : "text-rose-500 dark:text-rose-300"}>{passwordChecks.number ? "OK" : "X"} At least one number</div>
        </div>

        <button class="inline-flex w-full items-center justify-center rounded-2xl bg-gradient-to-r from-cyan-500 to-violet px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-cyan-500/20 transition duration-200 hover:-translate-y-0.5 hover:from-cyan-400 hover:to-fuchsia-500" on:click={submitRegister} disabled={loading}>
          {loading ? "Creating account..." : "Create account"}
        </button>
      </div>
    {/if}
  </div>
</section>
