 /* Script code for running labelling api */
// const toggleButton = document.getElementById("toggle_input");
//  const runScriptButton = document.getElementById("runScriptButton");
//
//  toggleButton.addEventListener("click", () => {
//    // Enable or disable the "Run Script" button based on the checkbox state
//    runScriptButton.disabled = !toggleButton.checked;
//  });
//
//  runScriptButton.addEventListener("click", () => {
//    fetch('/labelling', {
//      method: 'POST',
//    })
//    .then(response => response.text())
//    .then(data => {
//      console.log(data);
//    })
//    .catch(error => {
//      console.error("Error:", error);
//    });
//  });

const toggleButton = document.getElementById("toggle_input");

toggleButton.addEventListener("change", () => {
  if (toggleButton.checked) {
    // Make an API request when the checkbox is checked
    // You can use the Fetch API to make the request
    fetch('/labelling', {
      method: 'POST'
    })
    .then(response => response.text())
    .then(data => {
//      console.log(data);
      console.log("Labelling Api Started");
    })
    .catch(error => {
      console.error("Error:", error);
    });
  }
});

const toggleButton1 = document.getElementById("toggle_input1");

toggleButton1.addEventListener("change", () => {
  if (toggleButton1.checked) {
    // Make an API request when the checkbox is checked
    // You can use the Fetch API to make the request
    fetch('/training', {
      method: 'POST'
    })
    .then(response => response.text())
    .then(data => {
//      console.log(data);
      console.log("Training Api Started");
    })
    .catch(error => {
      console.error("Error:", error);
    });
  }
});

const toggleButton2 = document.getElementById("toggle_input2");

toggleButton2.addEventListener("change", () => {
  if (toggleButton2.checked) {
    // Make an API request when the checkbox is checked
    // You can use the Fetch API to make the request
    fetch('/conversion', {
      method: 'POST'
    })
    .then(response => response.text())
    .then(data => {
//      console.log(data);
      console.log("Conversion Api Started");
    })
    .catch(error => {
      console.error("Error:", error);
    });
  }
});

const toggleButton3 = document.getElementById("toggle_input3");

toggleButton3.addEventListener("change", () => {
  if (toggleButton3.checked) {
    // Make an API request when the checkbox is checked
    // You can use the Fetch API to make the request
    fetch('/detection', {
      method: 'POST'
    })
    .then(response => response.text())
    .then(data => {
//      console.log(data);
      console.log("Detection Api Started");
    })
    .catch(error => {
      console.error("Error:", error);
    });
  }
});

const toggleButton4 = document.getElementById("toggle_input4");

toggleButton4.addEventListener("change", () => {
  if (toggleButton4.checked) {
    // Make an API request when the checkbox is checked
    // You can use the Fetch API to make the request
    fetch('/prediction', {
      method: 'POST'
    })
    .then(response => response.text())
    .then(data => {
//      console.log(data);
      console.log("Prediction Api Started");
    })
    .catch(error => {
      console.error("Error:", error);
    });
  }
});

const toggleButton5 = document.getElementById("toggle_input5");

toggleButton5.addEventListener("change", () => {
  if (toggleButton4.checked) {
    // Make an API request when the checkbox is checked
    // You can use the Fetch API to make the request
    fetch('/pushtoS3', {
      method: 'POST'
    })
    .then(response => response.text())
    .then(data => {
//      console.log(data);
      console.log("Push S3 Api Started");
    })
    .catch(error => {
      console.error("Error:", error);
    });
  }
});