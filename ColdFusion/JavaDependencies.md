# Dependencies (incorporating Maven or finding missing dependencies/jars)

(Suggestions from Brad Wood)

If the jars don't have dependencies, I just use my box.json so my box install downloads them
using the jar: endpoint like so:
https://github.com/Ortus-Solutions/RabbitSDK/blob/development/box.json#L24

```json
"dependencies":{
    "amqp-client-5.9.0":"jar:https://repo1.maven.org/maven2/com/rabbitmq/amqp-client/5.9.0/amqp-client-5.9.0.jar"
},
```

Which will go under your lib folder unless you specify an installPath elsewhere

If you want maven dependencies pulled,
@foundeo has a CommandBox module for that: https://forgebox.io/view/maven-command
Were also looking to add a proper maven endpoint into CommandBox as well

### POM.xml or Java Tools

- See [Maven Integration with Lucee v6](https://dev.lucee.org/t/interacting-with-java-libraries-in-lucee-6-2/14362)

There's nothing in particular preventing you from using a POM.xml or build.gradle and using traditional java tools to get the jar. I'm just not a fan of introducing an entire separate toolchain just to do some basic HTTP downloads at the end of the day

Of course, the irony is, a LOT of people just commit the jars and are done with it, but please don't do that to your repo

### \*\*Use Maven to extract urls you need for missing JARs

what I'll do sometimes is put the dependency in a pom file, run a local install via maven and the just go back and take all the URLs it downloaded and slap them into my box.json manually

That's what I did here
https://github.com/coldbox-modules/GrowthBookSDK/blob/master/box.json#L2-L26

Because there were so many deps

if you download the maven binary, you should be able to run something like this
`mvn dependency:copy-dependencies -DincludeScope=runtime -DoutputDirectory=libs -Dartifact=com.github.growthbook:growthbook-sdk-java:0.9.9`
in an empty folder

replace `com.github.growthbook:growthbook-sdk-java:0.9.9` with your actual `org:package:version`

It should get your lib and all its dependencies into a local lib folder and you can parse to output of the command to see what it downloaded and from where, which, you could include Maven in your build and just make that be what you run- or extract all the jar paths from that little experiment and populate your box.json with them

It won't be the most fun 20-30 minutes of your life, but once you track down all the little buggers, it will work pretty good

Also, make sure your application.cfc is looking recursively like my repo shows as CommandBox will put each jar into a subfolder

I do something like this:

```java
this.javaSettings = {
	loadPaths = directorylist( expandPath( '/modules/GrowthBookSDK/lib' ), true, 'array', '*jar' ),
	loadColdFusionClassPath = true,
	reloadOnChange = false
};
```

I'm never really sure if CF does a recursive lookup or not, and it's complete and total lack of errors messages, logging, and good docs always leaves you wondering if it "worked" or not

Adjust the path in that code sample to point to your lib folder and it will be sure ot load them all

Or, if you're using CommandBox's `app.libDirs` in your `server.json`, it's already recursive

## Using OSGi

- https://www.codersrevolution.com/blog/using-osgi-to-load-a-conflicting-jar-into-lucee-server.print
