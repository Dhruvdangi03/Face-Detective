//=========================== function to remove landing page ================

const landing  = () => {
    var d = document.getElementById("screen1");
    d.style.transform = "translateY(100%)";
    setTimeout(()=>{
        d.style.display = "none";
    },500);
}

//==================================== Drop-zone logic ==========================

document.querySelectorAll(".drop-zone-input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    dropZoneElement.addEventListener("click", (e) => {
		inputElement.click();
	});

    dropZoneElement.addEventListener("dragover", (e) => {
		e.preventDefault();
		dropZoneElement.classList.add("drop-zone-active");
	});

    ["dragleave", "dragend"].forEach((type) => {
		dropZoneElement.addEventListener(type, (e) => {
			dropZoneElement.classList.remove("drop-zone-active");
		});
	});

    dropZoneElement.addEventListener("drop", (e) => {
		e.preventDefault();

		if (e.dataTransfer.files.length) {
			inputElement.files = e.dataTransfer.files;
			updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
		}

		dropZoneElement.classList.remove("drop-zone--over");
	});
});

//====================== function to show thumbnail ========================


/**
 * Updates the thumbnail on a drop zone element.
 *
 * @param {HTMLElement} dropZoneElement
 * @param {File} file
 */
function updateThumbnail(dropZoneElement, file) {
	let thumbnailElement = dropZoneElement.querySelector(".drop-zone-thumb");

	// First time - remove the prompt
	if (dropZoneElement.querySelector(".drop-zone-message")) {
		dropZoneElement.querySelector(".drop-zone-message").remove();
	}

	// First time - there is no thumbnail element, so lets create it
	if (!thumbnailElement) {
		thumbnailElement = document.createElement("div");
		thumbnailElement.classList.add("drop-zone-thumb");
		dropZoneElement.appendChild(thumbnailElement);
	}

	thumbnailElement.dataset.label = file.name;

	// Show thumbnail for image files
	if (file.type.startsWith("image/")) {
		const reader = new FileReader();

		reader.readAsDataURL(file);
		reader.onload = () => {
			thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
		};
	} else {
		thumbnailElement.style.backgroundImage = null;
	}
}

