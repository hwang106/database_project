let classYear = document.querySelector("#class-years");

function loadClassYears() {
    startingYear = 2000;
    endingYear = new Date().getFullYear();
    for(year = startingYear; year <= endingYear; year++){
        classYear.innerHTML += "<option value = '" + year + "'> Class of " + year + "</option>";
    }
}
