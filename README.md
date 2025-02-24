Install dependencies:

```
$ pipenv install
```

Make sure the CLERK_SECRET_KEY environment variable is set, ie:

```
$ export CLERK_SECRET_KEY=my_secret_key
```

Start the server:

```
$ pipenv run fastapi dev app/main
```

From a Clerk frontend, use the useSession hook to retrieve the getToken() function:

```js
const session = useSession();
const getToken = session?.session?.getToken

Then, request the python server:

if (getToken) {
    // get the userId or None if the token is invalid
    const res = await fetch("http://localhost:8000/clerk_jwt", {
        headers: {
            "Authorization": `Bearer ${await getToken()}`
        }
    })
    console.log(await res.json()) // {userId: 'the_user_id_or_null'}

    // get gated data or a 401 Unauthorized if the token is not valid
    const res = await fetch("http://localhost:8000/gated_data", {
        headers: {
            "Authorization": `Bearer ${await getToken()}`
        }
    })
    if (res.status === 401) {
        // token was invalid
    } else {
        console.log(await res.json()) // {foo: "bar"}
    }
}
```