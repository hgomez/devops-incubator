package basic

import com.excilys.ebi.gatling.core.Predef._
import com.excilys.ebi.gatling.http.Predef._
import com.excilys.ebi.gatling.jdbc.Predef._
import com.excilys.ebi.gatling.http.Headers.Names._
import akka.util.duration._
import bootstrap._

class BasicExampleSimulation extends Simulation {

	val extHost = Option(System.getProperty("host")).getOrElse("localhost")
	val extPort = Integer.getInteger("port", 8081)
	val extUsers = Integer.getInteger("users", 1)
	val extRampup = Integer.getInteger("rampup", 0).toLong
	val extPause = Integer.getInteger("pause", 1).toLong

	val extBaseUrl = if (extPort == 443)
		"https://" + extHost
	else if (extPort != 80)
		"http://" + extHost + ":" + extPort
	else
		"http://" + extHost

	val extWebapp = Option(System.getProperty("webapp")).getOrElse("/basic-perf/")

	val httpConf = httpConfig
		.baseURL(extBaseUrl)
		.acceptCharsetHeader("ISO-8859-1,utf-8;q=0.7,*;q=0.7")
		.acceptHeader("text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
		.acceptEncodingHeader("gzip, deflate")
		.acceptLanguageHeader("fr,fr-fr;q=0.8,en-us;q=0.5,en;q=0.3")
		.disableFollowRedirect

	val headers_1 = Map(
		"Keep-Alive" -> "115")

	val scn = scenario("Scenario name")
		.exec(
			http("PerfMeter")
				.get(extWebapp + "PerfMeter")
				.headers(headers_1)
				.check(status.is(200)))
		.pause(extPause milliseconds)
		.exec(
			http("PerfMeter-W100-RESP10K")
				.get(extWebapp + "PerfMeter?waittime=100&responsesize=102400")
				.headers(headers_1)
				.check(status.is(200)))
		.pause(extPause milliseconds)
		.exec(
			http("PerfMeter-W10000-NORESP")
				.get(extWebapp + "PerfMeter?waittime=10000&responsesize=-1")
				.headers(headers_1)
				.check(status.is(200)))
		.pause(extPause milliseconds)
		.exec(
			http("PerfMeter-NOW-RESP4K")
				.get(extWebapp + "PerfMeter?waittime=-1&responsesize=4096&response=PerfMe")
				.headers(headers_1)
				.check(status.is(200)))
		.pause(extPause milliseconds)

	setUp(scn.users(extUsers).ramp(extRampup).protocolConfig(httpConf))
}
