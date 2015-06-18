package basic

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class BasicPerfSimulation extends Simulation {

	val extHost = Option(System.getProperty("extHost")).getOrElse("localhost")
	val extPort = Integer.getInteger("extPort", 8081)
	val extUsers = Integer.getInteger("extUsers", 1).toInt
	val extRampup = Integer.getInteger("extRampup", 0).toInt
	val extPause = Integer.getInteger("extPause", 1).toLong
 	val extLoop = Integer.getInteger("extLoop", 100).toInt

	val extBaseUrl = if (extPort == 443)
		"https://" + extHost
	else if (extPort != 80)
		"http://" + extHost + ":" + extPort
	else
		"http://" + extHost

	val extWebapp = Option(System.getProperty("extWebapp")).getOrElse("/basic-perf/")

	val httpConf = http
		.baseURL(extBaseUrl)
		.acceptCharsetHeader("ISO-8859-1,utf-8;q=0.7,*;q=0.7")
		.acceptHeader("text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
		.acceptEncodingHeader("gzip, deflate")
		.acceptLanguageHeader("fr,fr-fr;q=0.8,en-us;q=0.5,en;q=0.3")
		.disableFollowRedirect

	val headers = Map(
		"Keep-Alive" -> "115")

	val scn = scenario("Scenario name")
		.repeat(extLoop) {
		exec(
			http("PerfMeter")
				.get(extWebapp + "PerfMeter")
				.headers(headers)
				.check(status.is(200)))
		.pause(extPause milliseconds)
		.exec(
			http("PerfMeter-W100ns-RESP10K")
				.get(extWebapp + "PerfMeter?waittime=100&responsesize=102400")
				.headers(headers)
				.check(status.is(200)))
		.pause(extPause milliseconds)
		.exec(
			http("PerfMeter-W10ms-NORESP")
				.get(extWebapp + "PerfMeter?waittime=10000&responsesize=-1")
				.headers(headers)
				.check(status.is(200)))
		.pause(extPause milliseconds)
		.exec(
			http("PerfMeter-W500ms-NORESP")
				.get(extWebapp + "PerfMeter?waittime=500000&responsesize=-1")
				.headers(headers)
				.check(status.is(200)))
		.pause(extPause milliseconds)
		.exec(
			http("PerfMeter-W0s-RESP4K")
				.get(extWebapp + "PerfMeter?waittime=-1&responsesize=4096&response=PerfMe")
				.headers(headers)
				.check(status.is(200)))
		.pause(extPause milliseconds)
		}
		
  setUp(
    scn.inject(
      atOnceUsers(extUsers), 
     rampUsers(extRampup) over(1 seconds)
    ).protocols(httpConf)
  )
}
