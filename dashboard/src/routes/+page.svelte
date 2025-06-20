<script lang="ts">
	import { SignedIn, SignedOut, SignInButton, UserButton } from 'svelte-clerk/client';
</script>


    
	<header>
		<SignedOut>
            Sign In:
			<SignInButton />
		</SignedOut>
		<SignedIn>
            Welcome to the new Roshid, bitches!!!
			<UserButton />

            <a href="/logged">Go to Logged In Page</a>

		</SignedIn>
	</header>
