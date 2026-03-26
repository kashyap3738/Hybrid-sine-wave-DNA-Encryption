<script>
  import { onMount } from "svelte";
  import AuthPanel from "./lib/components/AuthPanel.svelte";
  import EncryptShareTab from "./lib/components/EncryptShareTab.svelte";
  import SentTab from "./lib/components/SentTab.svelte";
  import ReceivedTab from "./lib/components/ReceivedTab.svelte";
  import DecryptTab from "./lib/components/DecryptTab.svelte";
  import AnalyticsTab from "./lib/components/AnalyticsTab.svelte";
  import ProfileTab from "./lib/components/ProfileTab.svelte";
  import LandingPage from "./lib/components/LandingPage.svelte";
  import ThemeToggle from "./lib/components/ThemeToggle.svelte";
  import { api, setToken } from "./lib/api.js";

  const tabs = ["Encrypt & Share", "Sent", "Received", "Decrypt", "Analytics", "Profile"];

  let activeTab = tabs[0];
  let loading = false;
  let authError = "";
  let registerError = "";
  let registerSuccess = "";

  let currentUser = null;
  let stats = null;
  let otherUsers = [];
  let sentData = { images: [], shared_history: [] };
  let receivedShares = [];
  let theme = "light";
  let publicPage = "landing";
  let authMode = "login";

  function applyTheme(nextTheme) {
    theme = nextTheme;
    document.documentElement.classList.toggle("dark", theme === "dark");
    localStorage.setItem("dna-theme", theme);
  }

  function toggleTheme() {
    applyTheme(theme === "dark" ? "light" : "dark");
  }

  async function bootstrap() {
    const storedTheme = localStorage.getItem("dna-theme");
    const preferredDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    applyTheme(storedTheme || (preferredDark ? "dark" : "light"));

    if (!api.token) return;
    try {
      const me = await api.getMe();
      currentUser = me.user;
      stats = me.stats;
      await refreshDashboard();
    } catch (error) {
      setToken("");
    }
  }

  async function refreshDashboard() {
    if (!currentUser) return;
    const [usersResponse, sentResponse, receivedResponse, meResponse] = await Promise.all([
      api.getOtherUsers(),
      api.getSent(),
      api.getReceived(),
      api.getMe()
    ]);
    otherUsers = usersResponse.users;
    sentData = sentResponse;
    receivedShares = receivedResponse.shares;
    stats = meResponse.stats;
  }

  async function handleLogin(event) {
    loading = true;
    authError = "";
    registerError = "";
    registerSuccess = "";

    try {
      const response = await api.login(event.detail);
      setToken(response.token);
      currentUser = response.user;
      await refreshDashboard();
    } catch (error) {
      authError = error.message;
    } finally {
      loading = false;
    }
  }

  async function handleRegister(event) {
    loading = true;
    registerError = "";
    registerSuccess = "";

    try {
      const response = await api.register(event.detail);
      registerSuccess = response.message;
    } catch (error) {
      registerError = error.message;
    } finally {
      loading = false;
    }
  }

  async function handleLogout() {
    try {
      await api.logout();
    } catch (error) {
      // Preserve logout UX even if backend is unreachable.
    }
    setToken("");
    currentUser = null;
    stats = null;
    otherUsers = [];
    sentData = { images: [], shared_history: [] };
    receivedShares = [];
    activeTab = tabs[0];
    publicPage = "landing";
  }

  function openAuth(mode = "login") {
    authMode = mode;
    publicPage = "auth";
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function openLandingFeatures() {
    const features = document.getElementById("features");
    if (features) {
      features.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  onMount(bootstrap);
</script>

<ThemeToggle {theme} onToggle={toggleTheme} />

{#if !currentUser}
  {#if publicPage === "landing"}
    <LandingPage onGetStarted={() => openAuth("login")} onLearnMore={openLandingFeatures} />
  {:else}
    <AuthPanel
      {loading}
      error={authError}
      {registerError}
      {registerSuccess}
      initialMode={authMode}
      onBack={() => (publicPage = "landing")}
      on:login={handleLogin}
      on:register={handleRegister}
    />
  {/if}
{:else}
  <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
    <section class="panel overflow-hidden p-8">
      <div class="flex flex-col gap-6 xl:flex-row xl:items-end xl:justify-between">
        <div>
          <div class="inline-flex rounded-full bg-teal/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.25em] text-teal dark:bg-cyan-500/10 dark:text-cyan-300">
            Hybrid Sine-Wave DNA Encryption
          </div>
          <h1 class="mt-4 font-display text-4xl font-bold tracking-tight">Welcome, {currentUser.username}</h1>
          <p class="mt-2 text-base text-slate-600 dark:text-slate-300">Encrypt, share, decrypt, and verify images securely.</p>
        </div>
        <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
          <div class="metric-card">
            <div class="text-xs uppercase tracking-[0.2em] text-slate-400 dark:text-slate-500">Encrypted</div>
            <div class="mt-2 text-2xl font-semibold">{stats?.total_encrypted || 0}</div>
          </div>
          <div class="metric-card">
            <div class="text-xs uppercase tracking-[0.2em] text-slate-400 dark:text-slate-500">Sent</div>
            <div class="mt-2 text-2xl font-semibold">{stats?.total_sent || 0}</div>
          </div>
          <div class="metric-card">
            <div class="text-xs uppercase tracking-[0.2em] text-slate-400 dark:text-slate-500">Received</div>
            <div class="mt-2 text-2xl font-semibold">{stats?.total_received || 0}</div>
          </div>
        </div>
      </div>

      <div class="mt-8 flex flex-wrap gap-3">
        {#each tabs as tab}
          <button class={`tab-button ${activeTab === tab ? "tab-active" : "tab-inactive"}`} on:click={() => (activeTab = tab)}>
            {tab}
          </button>
        {/each}
      </div>
    </section>

    <section class="mt-6">
      {#if activeTab === "Encrypt & Share"}
        <EncryptShareTab users={otherUsers} onRefresh={refreshDashboard} />
      {:else if activeTab === "Sent"}
        <SentTab data={sentData} />
      {:else if activeTab === "Received"}
        <ReceivedTab shares={receivedShares} />
      {:else if activeTab === "Decrypt"}
        <DecryptTab shares={receivedShares} />
      {:else if activeTab === "Analytics"}
        <AnalyticsTab images={sentData.images} />
      {:else if activeTab === "Profile"}
        <ProfileTab user={currentUser} {stats} onLogout={handleLogout} />
      {/if}
    </section>
  </main>
{/if}
