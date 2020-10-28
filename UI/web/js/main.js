//Normal JS Functions

function hideAll() {
    let homeComponent = document.getElementById("homeComponent");
    let createTest = document.getElementById("createTest");
    let runWindow = document.getElementById("runWindow");
    createTest.style.display = "none";
    runWindow.style.display = "none";
    homeComponent.style.display = "block";

}
function displayCreateTest() {
    let createTest = document.getElementById("createTest");
    let runWindow = document.getElementById("runWindow");
    createTest.style.display = "block";
    runWindow.style.display = "none";
    homeComponent.style.display = "none";

}
function displayRunWindow() {
    document.getElementById("loading").style.display = "none";
    let createTest = document.getElementById("createTest");
    let runWindow = document.getElementById("runWindow");
    createTest.style.display = "none";
    runWindow.style.display = "block";
    homeComponent.style.display = "none";

}

function createTitle(value) {
    dataView = document.getElementById("data");
    summaryView = document.getElementById("summary");
    var name = document.createElement("h5")
    var textnode = document.createTextNode(value);
    name.style.color = "#fff";
    name.style.marginTop= "10px"
    name.appendChild(textnode);
    dataView.appendChild(name);
}

function displayTestReport(value) {
    dataView = document.getElementById("data");
    for (var i = 0; i < value.length; i++) {
        var line = document.createElement('p');
        var text = value[i];

        if (text.split(" ")[0].includes("test")) {
            var textnode = document.createTextNode(text.replace(text.split(" ")[1], ''));
            console.log(text.split(" ")[1]);
            line.style.color = setColor(text.split(" ")[1]);
            line.appendChild(textnode);
            dataView.appendChild(line);

        } else {
            var textnode = document.createTextNode(text);
            console.log(text);
            if (text.split(" ")[0] == "Compile") {
                textnode = document.createTextNode(text.split(" ")[0] + " " + text.split(" ")[1]);
                line.style.color = setColor(text.split(" ")[text.split(" ").length - 1]);
                line.appendChild(textnode);
                dataView.appendChild(line);
            } else if (text.includes("TotalMarks")) {
                var total = document.createElement('h3');
                var tn = document.createTextNode("Total Marks");
                total.appendChild(tn);
                total.style.color = "#fff";
                dataView.appendChild(total);
            } else {
                var marks = document.createElement('h4')
                textnode = document.createTextNode(text.split("=")[1]);
                marks.style.color = setColor(text.split(" ")[text.split(" ").length - 1]);
                marks.style.marginLeft = "20px";
                marks.style.color = "#fff";
                marks.appendChild(textnode);
                dataView.appendChild(marks);

            }
        }
    }

}

function setColor(value) {
    var colors = ["ORANGE", "GREEN", "RED:", "BLUE"]
    var hexColors = ["#fb8a2e", "#7fbb00", "#ff0b00", "#009fe3"]

    return hexColors[colors.indexOf(value)]
}


//EEl Functions
function helloMe() {
    let data = document.getElementById("data");

    //python
    eel.helloPy()(function (ret) { console.log(ret) })
}

function autocheckFiles() {
    
    subDir = document.getElementById("submissionDir");
    testDir = document.getElementById("testDir")

    if (subDir.textContent && testDir.textContent) {
        document.getElementById("loading").style.display = "block";
        eel.autocheckMe()((ret) => {
            console.log(ret);
            var jsonObj = JSON.parse(ret);
            console.log(jsonObj);

            for (var i = 0; i < jsonObj.data.length; i++) {
                createTitle(jsonObj.data[i].name);
                displayTestReport(jsonObj.data[i].tests);

                var seperator = document.createElement('hr');
                seperator.class = "my-4 text-white";
                document.getElementById("data").appendChild(seperator);
            }
            document.getElementById("loading").style.display = "none";
        });
    }else{
        alert("Select Directories");
    }

}




function loadSubmissionFolder() {
    eel.fileLocationSub()((folderPath) => {
        var submission = document.getElementById("submissionDir");
        var textnode = document.createTextNode(folderPath);
        submission.appendChild(textnode);

    });
}

function loadTestsFolder() {
    eel.fileLocationTest()((folderPath) => {
        var submission = document.getElementById("testDir");
        var textnode = document.createTextNode(folderPath);
        submission.appendChild(textnode);

    });
}



