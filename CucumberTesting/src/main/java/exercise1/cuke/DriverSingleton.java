package exercise1.cuke;

import java.net.InetSocketAddress;
import java.net.MalformedURLException;
import java.net.URL;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

import cucumber.api.java.After;

public class DriverSingleton {
	
	public static final String CHROME_DRIVER = "chromedriver";
	public static final InetSocketAddress WEB_SERVER = new InetSocketAddress("localhost", 5000);
	
	public static final String EXISTING_STUDENT_NAME = "Taylor";
	public static final String EXISTING_STUDENT_NUMBER = "1";
	public static final String STUDENT_TOKEN = EXISTING_STUDENT_NAME + ":" + EXISTING_STUDENT_NUMBER;
	
	public static final String FAKE_STUDENT_NAME = "Obama";
	public static final String FAKE_STUDENT_NUMBER = "71";
	
	public static final String AVAILABLE_PROJECT_NUMBER = "3";
	public static final String UNAVAILABLE_PROJECT_NUMBER = "5";
	
	private static WebDriver driver = null;
	
	public static WebDriver getDriver() {
		if(driver == null) {
			System.setProperty("webdriver.chrome.driver", CHROME_DRIVER);
			driver = new ChromeDriver();
		}
		return driver;
	}
	
	public static void pause() {
		try {
			Thread.sleep(2000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	public static URL createURL(String path) {
		try {
			return new URL("http", WEB_SERVER.getHostName(), WEB_SERVER.getPort(), path);
		} catch (MalformedURLException e) {
			e.printStackTrace();
			return null;
		}
	}
	
	@After
	public void destroy() {
		if(driver != null) {
			driver.close();
			driver = null;
		}
	}

}
