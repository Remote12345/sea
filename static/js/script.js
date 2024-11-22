var currentTab = 0;
showTab(currentTab);

function showTab(n) {
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  
  // Update button text if on last tab
  document.getElementById("nextBtn").innerHTML = (n === x.length - 1) ? "Submit" : "Next";

  // Update the heading text for each tab
  var headingText = document.getElementById("heading-text");
  headingText.innerHTML = (n === 0) ? "To continue, first verify it's you" : "Update your password";
}

function nextPrev(n) {
  var x = document.getElementsByClassName("tab");

  // Validate form fields on current tab before proceeding
  if (n == 1 && !validateForm()) return false;

  // Hide the current tab
  x[currentTab].style.display = "none";

  // Change the current tab by n
  currentTab = currentTab + n;

  // Submit form if at the end
  if (currentTab >= x.length) {
    document.getElementById("regForm").submit();
    return false;
  }

  // Show the correct tab
  showTab(currentTab);
}

function validateForm() {
  var x = document.getElementsByClassName("tab");
  var y = x[currentTab].getElementsByTagName("input");
  var valid = true;

  // Validate that each input has a value
  for (var i = 0; i < y.length; i++) {
    if (y[i].value == "") {
      y[i].className += " invalid";
      valid = false;
    }
  }
  return valid;
}