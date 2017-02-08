package exercise1.cuke;

import org.openqa.selenium.By;
import org.openqa.selenium.Cookie;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import static org.junit.Assert.*;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;

import static exercise1.cuke.DriverSingleton.*;

public class StudentLogin {
	
	@Given("^User is not yet logged in as student$")
	public void studentNotSignedIn() {
		DriverSingleton.getDriver().manage().deleteCookie(new Cookie("studenttoken", ""));
	}

	@Given("^User navigated to student login$")
	public void navigatedToStudentLogin() {
		getDriver().navigate().to(createURL("/students/login"));
		pause();
	}

	@When("^User logs in as an existing student$")
	public void existingStudentLogin() {
		loginAs(EXISTING_STUDENT_NAME, EXISTING_STUDENT_NUMBER);
	}

	@When("^User logs in as a fake student$")
	public void fakeStudentLogin() {
		loginAs(FAKE_STUDENT_NAME, FAKE_STUDENT_NUMBER);
	}
	
	private void loginAs(String name, String number) {
		WebDriver driver = getDriver();
		WebElement element = driver.findElement(By.id("student_name_field"));
		element.sendKeys(name);
		element = driver.findElement(By.id("student_number_field"));
		element.sendKeys(number);
		pause();
		element.submit();
	}
	
	@Then("^User is finally logged in as a student$")
	public void studentLoggedIn() {
		assertEquals(STUDENT_TOKEN, getDriver().manage().getCookieNamed("studenttoken").getValue());
	}
	
	@Then("^User is not logged in as a student$")
	public void studentNotLoggedIn() {
		pause();
		assertEquals(null, getDriver().manage().getCookieNamed("studenttoken"));
	}
}
