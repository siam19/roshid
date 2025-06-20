<script lang="ts">
	import { useClerkContext } from 'svelte-clerk/client';

	// Do not destructure context to avoid losing reactivity
	const ctx = useClerkContext();

	const userId = $derived(ctx.auth.userId);
    const username = $derived(ctx.user.username);
    const sessionId = $derived(ctx.auth.sessionId);
    const token = $derived(ctx.session.getToken());

	const fetchUserInformation = async () => {
	console.log('User ID:', userId);
    console.log('Username:', username);
    console.log('Session ID:', sessionId);
    console.log('Token:', token);
	};

    fetchUserInformation();
</script>

{#if userId === undefined}
	<p>Loading...</p>
{:else if userId === null}
	<p>Sign in to view this page</p>
{:else}
	<div>...</div>
{/if}