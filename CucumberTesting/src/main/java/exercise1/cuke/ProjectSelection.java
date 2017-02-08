package exercise1.cuke;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;

import static org.junit.Assert.*;

import org.openqa.selenium.By;
import org.openqa.selenium.Cookie;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import static exercise1.cuke.DriverSingleton.*;

public class ProjectSelection {
	
	@Given("^User is already logged in as a student$")
	public void onProjectSlectionPage() {
		WebDriver driver = getDriver();
		driver.navigate().to(createURL("/"));
		driver.manage().addCookie(new Cookie("studenttoken", STUDENT_TOKEN));
	}
	
	@Given("^User is already on project selection page$")
	public void alreadyOnProjectPage() {
		getDriver().navigate().to(createURL("/students/view"));
		pause();
	}
	
	@When("^User selects an available project$")
	public void availableProjectSelection() {
		selectProject(AVAILABLE_PROJECT_NUMBER);
	}
	
	@When("^User selects an unavailable project$")
	public void unavailableProjectSelection() {
		selectProject(UNAVAILABLE_PROJECT_NUMBER);
	}
	
	@Then("^Project selection is finally accepted$")
	public void selectionConfirmed() {
		selectionConfirmation("accepted");
	}
	
	@Then("^Project selection is finally denied$")
	public void selectionDenied() {
		selectionConfirmation("denied");
	}
	
	private void selectProject(String number) {
		WebElement radioItem = getDriver().findElement(By.id("project_" + number));
		radioItem.click();
		pause();
		radioItem.submit();
	}
	
	public void selectionConfirmation(String cls) {
		WebElement confMsg = getDriver().findElement(By.id("confirmation"));
		pause();
		assertEquals(confMsg.getAttribute("class"), cls);
	}
	
	
}
