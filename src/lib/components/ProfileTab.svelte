<script>
  import ResultDisplay from "./ResultDisplay.svelte";
  import { api } from "../api.js";

  export let user = null;
  export let stats = null;
  export let onLogout = async () => {};

  let currentPassword = "";
  let newPassword = "";
  let confirmPassword = "";
  let message = "";
  let tone = "info";
  let loading = false;

  async function updatePassword() {
    loading = true;
    try {
      const response = await api.changePassword({
        current_password: currentPassword,
        new_password: newPassword,
        confirm_password: confirmPassword
      });
      message = response.message;
      tone = "success";
      currentPassword = "";
      newPassword = "";
      confirmPassword = "";
    } catch (error) {
      message = error.message;
      tone = "error";
    } finally {
      loading = false;
    }
  }
</script>

<div class="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
  <div class="panel p-6">
    <div class="flex items-center gap-4">
      <div class="flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-coral to-teal text-xl font-bold text-white">
        {user?.username?.slice(0, 2)?.toUpperCase()}
      </div>
      <div>
        <h3 class="font-display text-xl font-semibold">{user?.username}</h3>
        <p class="text-sm text-slate-500 dark:text-slate-400">Member since {stats?.created_at}</p>
      </div>
    </div>

    <div class="mt-6 grid gap-4 sm:grid-cols-3">
      <div class="soft-card p-4">
        <div class="text-xs uppercase tracking-[0.2em] text-slate-400 dark:text-slate-500">Encrypted</div>
        <div class="mt-2 text-2xl font-semibold">{stats?.total_encrypted || 0}</div>
      </div>
      <div class="soft-card p-4">
        <div class="text-xs uppercase tracking-[0.2em] text-slate-400 dark:text-slate-500">Sent</div>
        <div class="mt-2 text-2xl font-semibold">{stats?.total_sent || 0}</div>
      </div>
      <div class="soft-card p-4">
        <div class="text-xs uppercase tracking-[0.2em] text-slate-400 dark:text-slate-500">Received</div>
        <div class="mt-2 text-2xl font-semibold">{stats?.total_received || 0}</div>
      </div>
    </div>

    <button class="btn-secondary mt-6 w-full" on:click={onLogout}>Sign out</button>
  </div>

  <div class="panel p-6">
    <h3 class="font-display text-lg font-semibold">Change Password</h3>
    <div class="mt-4 space-y-4">
      <div>
        <label class="label">Current password</label>
        <input class="input" type="password" bind:value={currentPassword} />
      </div>
      <div>
        <label class="label">New password</label>
        <input class="input" type="password" bind:value={newPassword} />
      </div>
      <div>
        <label class="label">Confirm new password</label>
        <input class="input" type="password" bind:value={confirmPassword} />
      </div>
      <button class="btn-primary w-full" on:click={updatePassword} disabled={loading}>
        {loading ? "Updating..." : "Update password"}
      </button>
    </div>

    {#if message}
      <div class="mt-6">
        <ResultDisplay title="Password status" type={tone} message={message} />
      </div>
    {/if}
  </div>
</div>
