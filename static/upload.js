// Wrap your JavaScript code in an event listener to ensure it runs after the DOM is ready
document.addEventListener("DOMContentLoaded", function () {
  var element = document.getElementById("upload-form-file");
  // console.log(element); // to debug
  if (element) {
    console.log("Element found: ", element.className);

    element.addEventListener("change", function (event) {
      // Access the selected files using the "files" property of the file input element
      var selectedFiles = event.target.files;

      // Do something with the selected files (e.g., display file names)
      if (selectedFiles.length > 0) {
        var fileList = document.getElementById("fileList");
        fileList.innerHTML = ""; // Clear the list before updating

        for (var i = 0; i < selectedFiles.length; i++) {
          var listItem = document.createElement("li");
          listItem.textContent = selectedFiles[i].name;
          fileList.appendChild(listItem);
        }
      }
    });
  } else {
    console.log("Element not found.");
  }
});
