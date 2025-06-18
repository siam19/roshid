<script lang="ts">
	import { SignedIn, SignedOut, SignInButton, UserButton } from 'svelte-clerk/client';
</script>


    
	<header>
		<SignedOut>
            Sign In:
			<SignInButton />
		</SignedOut>
		<SignedIn>
            Heyy
			<UserButton />
		</SignedIn>
	</header>
