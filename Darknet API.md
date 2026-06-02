**Source:** [bitburner.darknet.md](https://raw.githubusercontent.com/bitburner-official/bitburner-src/refs/heads/dev/markdown/bitburner.darknet.md) (dev branch)

This is a cleaned and annotated version of the official Darknet interface documentation with RAM costs added for convenience.

## Interface

```typescript
interface Darknet
```

## Methods

### authenticate(host, password, additionalMsec?)
Sends a network request to try to authenticate on a darkweb server. The target server must be directly connected to the server that the script is running on. The speed of authentication scales with the number of threads used.

If successful, grants the current script a session, allowing it to `exec()` scripts on that server, or `scp()` files to it. (`scp()` *from* the server is always allowed.)

Note that the charisma level on a server is not a requirement for authentication, but authentication takes longer if the player's charisma is below the server's charisma level.

Note that the session granted is only for the current script instance (by PID) — other running scripts will need to use `connectToSession` with the correct password to also get a session with the target server.

**RAM cost:** 0.4 GB

### connectToSession(host, password)
Attempts to connect to a target darkweb server that you have previously authenticated on. Unlike `authenticate`, `connectToSession` can be used to get a session on servers at any distance.

If successful, grants the script a session, allowing it to `scp()` files to that target. It also allows starting scripts with `exec()` on that target, if the target is directly connected to the server that the script is running on, or has a backdoor or stasis link.

**RAM cost:** 0.05 GB

### getBlockedRam(host?)
Gets the amount of RAM blocked by the server owner's processes. This ram can be freed for use using `dnet.memoryReallocation()`.

**RAM cost:** 0 GB

### getDarknetInstability()
Gets the current instability of the darknet caused by excessive backdoor-ing of servers.

**RAM cost:** 0 GB

### getDepth(host?)
Gets the current depth of the specified server into the darknet. Servers immediately below Darkweb are depth 0, and each visual row in the UI below that increases the depth of the server.

Returns -1 if the server is offline, not found, or not a darkweb server.

**RAM cost:** 0.1 GB

### getServerDetails(host?)
Returns the darknet-specific details of the server.

If the darknet server has recently gone offline, the returned object will be a dummy server object with `isOnline: false`.

**RAM cost:** 0.1 GB

### getServerRequiredCharismaLevel(host?)
Gets the required charisma level to target the server with `dnet.heartbleed()`.

Insufficient charisma will also cause authentication to take much longer — or, in certain servers deep in the darknet, be impossible.

**RAM cost:** 0.1 GB

### getStasisLinkedServers(returnByIP?)
Returns the hostnames/IPs of servers that have a stasis link applied.

**RAM cost:** 0 GB

### getStasisLinkLimit()
Returns the maximum number of stasis links that can be applied globally, based on the player's current status. Stasis link limit can be increased by finding special augmentations in the deep darknet.

**RAM cost:** 0 GB

### heartbleed(host, options?)
Uses an exploit to extract log data from a server by sending a malformed heartbeat request. Retrieves the most recent logs on the server. This can be used to get more feedback on authentication attempts. The retrieved logs are removed from the server, unless the `"peek"` flag is set to true in the provided `HeartbleedOptions`.

Servers will periodically produce logs themselves, as well, which sometimes are useful, but most times are not.

The speed of capture scales with the number of threads used.

**RAM cost:** 0.6 GB

### induceServerMigration(host)
Increases the chance that the target server will move to other parts of the darknet, by overloading the connections between it and the current server. The target must be a connected, non-stationary, darknet server — scripts cannot target the server they are running on.

Effect scales with threads and charisma level.

**RAM cost:** 4 GB

### isDarknetServer(host)
Returns whether the server is a darknet server.

Returns false if the server does not exist or has gone offline recently. This function does not require `DarkscapeNavigator.exe`.

**RAM cost:** 0.1 GB

### labradar()
There is more than meets the eye.

**RAM cost:** 0 GB

### labreport()
Not all who wander are lost.

**RAM cost:** 0 GB

### memoryReallocation(host?)
Spends some time freeing some of the RAM currently blocked by the server owner. Must target an authenticated and directly connected server.

The amount of ram recovered scales with charisma and the number of threads used.

**RAM cost:** 1 GB

### nextMutation()
Sleep until the next mutation of the network of darknet servers (which occur frequently). Note that in the majority of cases, whatever changed out on the net (if anything) will not be nearby to, or visible from, the current server.

**RAM cost:** 0 GB

### openCache(filename, suppressToast?)
Opens a `.cache` file on the current server to acquire its valuable contents.

**RAM cost:** 2 GB

### phishingAttack()
Spends time sending out phishing emails, attempting to find some non-technical middle manager to fall for the scam. Builds charisma. Often the attempt will fail, but success can be increased with crime success rate and charisma stats.

The amount of money lifted scales with the number of threads used, if successful. Very occasionally you can retrieve a cache file from the attempt.

Phishing attacks can only be run from scripts on darknet servers.

**RAM cost:** 2 GB

### probe(returnByIP?)
Returns a list of all darknet servers connected to the script's current server. For example, if called from a script running on `home`, it will return `["darkweb"]`. It will return an empty list if there are no darknet servers connected to the current server.

Note that there is no guarantee about the order of servers in the returned list.

**RAM cost:** 0.2 GB

### promoteStock(sym)
Spends some time spreading propaganda about a stock to increase its volatility. This does not actually change the stock's forecasts, but a savvy investor can take advantage of the chaos. The effect scales with charisma and the number of threads used, but degrades over time if left alone.

**RAM cost:** 2 GB

### setStasisLink(shouldLink?)
Applies or removes a stasis link to the script's current server. This will allow you to `connectToSession()` or `exec()` to the server remotely, even if it is not directly connected to the server a script is running on. It also allows direct connection to the server via the terminal.

Stasis links also prevent the server from going offline or moving.

**RAM cost:** 12 GB

### unleashStormSeed()
Executes `STORM_SEED.exe`, if it is present on the server the script is running on.

**Warning:** That exe file creates a webstorm that can cause catastrophic damage to the darknet. Run at your own risk.

**RAM cost:** 0.1 GB

---

*Note: All RAM costs above were taken directly from the official per-function documentation in the Bitburner source (dev branch). Verified as of latest fetch.*