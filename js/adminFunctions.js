// Shows the section to create a movie
function showCreate() {
    document.getElementById('showCreateButton').style.display = "none"
    document.getElementById('movieTable').style.display = "none"
    document.getElementById('createUpdateForm').style.display = "block"
    document.getElementById('iden').style.display = "none"
    document.getElementById('createLabel').style.display = "inline"
    document.getElementById('updateLabel').style.display = "none"
    document.getElementById('voteLabel').style.display = "none"
    document.getElementById('doCreateButton').style.display = "block"
    document.getElementById('doUpdateButton').style.display = "none"
    document.getElementById('dovoteButton').style.display = "none"
}
// Shows everything
function showViewAll() {
    document.getElementById('showCreateButton').style.display = "block"
    document.getElementById('movieTable').style.display = "block"
    document.getElementById('createUpdateForm').style.display = "none"
}
// Shows the edit movie form
function showUpdate(buttonElement) {
    document.getElementById('showCreateButton').style.display = "none"
    document.getElementById('movieTable').style.display = "none"
    document.getElementById('createUpdateForm').style.display = "block"
    document.getElementById('iden').style.display = "none"
    document.getElementById('createLabel').style.display = "none"
    document.getElementById('updateLabel').style.display = "inline"
    document.getElementById('voteLabel').style.display = "none"
    document.getElementById('doCreateButton').style.display = "none"
    document.getElementById('doUpdateButton').style.display = "block"
    document.getElementById('dovoteButton').style.display = "none"
    var rowElement = buttonElement.parentNode.parentNode
    // these is a way of finding the closest <tr> which would safer, closest()
    var movie = getmovieFromRow(rowElement)
    populateFormWithmovie(movie)
}
// Executes the function to create movie
function doCreate() {
    var form = document.getElementById('createUpdateForm')
    var movie = {}
    movie.name = form.querySelector('input[name="name"]').value
    movie.genre = form.querySelector('select[name="genre"]').value
    movie.description = form.querySelector('input[name="description"]').value

    // Error checking nothing to be left blank
    if (movie.name == "") {
        alert("Name must be filled in")
    }
    else if (movie.description == "") {
        alert("Description must be filled in")
    }
    else {
        // Call to ajax method to create movie on server
        createmovieAjax(movie)
        addmovieToTable(movie)
        clearForm()
        showViewAll()
        // Refreshes window to recall from db
        window.location.reload();
    }

}
// Function to edit the movie
function doUpdate() {
    var movie = getmovieFromForm();
    x = movie['description']
    // Error checking nothing to be left blank
    if (x == "") {
        alert("Description must be filled in")
    }
    // If it passes then do the update
    else {
        var rowElement = document.getElementById(movie.name);
        // Call to ajax method to update movie on server
        updatemovieAjax(movie);
        setmovieInRow(rowElement, movie);
        clearForm();
        showViewAll();
        // Refreshes window to recall from db
        window.location.reload();
    }
}

// Function to add/remove votes
function dovote() {
    var movie = getmovieFromForm2();
    var index = movie.id;
    // Gets movie from last cell in table
    var index = document.getElementById("movieTable").rows[index].lastChild.innerHTML
    var form = document.getElementById('createUpdateForm')
    var numvotes = form.querySelector('input[name="totalVotes"]').value
    // Call to ajax method to update movie on server
    votesAjax(index, numvotes);
    clearForm();
    showViewAll();
    // Refreshes window to recall from db
    window.location.reload();
}
// SHows the voting form
function showVote(buttonElement) {
    document.getElementById('showCreateButton').style.display = "none"
    document.getElementById('movieTable').style.display = "none"
    document.getElementById('createUpdateForm').style.display = "block"
    document.getElementById('votesform').style.display = "inline"
    document.getElementById('name').style.display = "none"
    document.getElementById('gen').style.display = "none"
    document.getElementById('iden').style.display = "none"
    document.getElementById('description').style.display = "none"
    document.getElementById('createLabel').style.display = "none"
    document.getElementById('updateLabel').style.display = "none"
    document.getElementById('voteLabel').style.display = "inline"
    document.getElementById('doCreateButton').style.display = "none"
    document.getElementById('doUpdateButton').style.display = "none"
    document.getElementById('dovoteButton').style.display = "block"
    var rowElement = buttonElement.parentNode.parentNode
    var id = rowElement.rowIndex
    var movie = getmovieFromRow(rowElement)
    populateFormWithmovie2(movie, id)
}
// Delete a movie
function doDelete(r) {
    var tableElement = document.getElementById('movieTable');
    var rowElement = r.parentNode.parentNode;
    var index = rowElement.rowIndex;
    // Call to ajax method to delete movie on server
    deletemovieAjax(rowElement.getAttribute("id"));
    tableElement.deleteRow(index);
}
// Populate table with movie from db and buttons
function addmovieToTable(movie) {
    var tableElement = document.getElementById('movieTable')
    var rowElement = tableElement.insertRow(-1)
    rowElement.setAttribute('id', movie.name)
    var cell1 = rowElement.insertCell(0);
    cell1.innerHTML = movie.name
    var cell2 = rowElement.insertCell(1);
    cell2.innerHTML = movie.genre
    var cell3 = rowElement.insertCell(2);
    cell3.innerHTML = movie.description
    var cell4 = rowElement.insertCell(3);
    cell4.innerHTML = movie.totalVotes
    var cell5 = rowElement.insertCell(4);
    cell5.innerHTML = '<button onclick="showUpdate(this)">Update</button>'
    var cell6 = rowElement.insertCell(5);
    cell6.innerHTML = '<button onclick=doDelete(this)>Delete</button>'
    var cell7 = rowElement.insertCell(6);
    cell7.innerHTML = '<button onclick=showVote(this)>Vote</button>'
    var cell8 = rowElement.insertCell(7);
    var x = movie.id
    cell8.innerHTML = movie.id
}
// Clears form so nothing is held
function clearForm() {
    var form = document.getElementById('createUpdateForm')
    form.querySelector('input[name="name"]').disabled = false
    form.querySelector('input[name="name"]').value = ''
    form.querySelector('select[name="genre"]').value = ''
    form.querySelector('input[name="description"]').value = ''
}
function getmovieFromRow(rowElement) {
    var movie = {}
    movie.name = rowElement.cells[0].firstChild.textContent
    movie.genre = rowElement.cells[1].firstChild.textContent
    movie.description = rowElement.cells[2].firstChild.textContent
    movie.totalVotes = parseInt(rowElement.cells[3].firstChild.textContent, 10)
    movie.id = parseInt(rowElement.cells[4].firstChild.textContent, 10)
    return movie
}
function setmovieInRow(rowElement, movie) {
    rowElement.cells[0].firstChild.textContent = movie.name
    rowElement.cells[1].firstChild.textContent = movie.genre
    rowElement.cells[2].firstChild.textContent = movie.description
    rowElement.cells[3].firstChild.textContent = movie.totalVotes
}
function populateFormWithmovie(movie) {
    var form = document.getElementById('createUpdateForm')
    form.querySelector('input[name="name"]').disabled = true
    form.querySelector('input[name="name"]').value = movie.name
    form.querySelector('select[name="genre"]').value = movie.genre
    form.querySelector('input[name="description"]').value = movie.description
    //form.querySelector('input[name="totalVotes"]').value= movie.totalVotes
    return movie
}
// Populate movie has ID aswell
function populateFormWithmovie2(movie, id) {
    var form = document.getElementById('createUpdateForm')
    form.querySelector('input[name="name"]').disabled = true
    form.querySelector('input[name="name"]').value = movie.name
    form.querySelector('select[name="genre"]').value = movie.genre
    form.querySelector('input[name="description"]').value = movie.description
    form.querySelector('input[name="iden"]').value = id
    return movie
}
// Get movie from form with ID aswell
function getmovieFromForm2() {
    var form = document.getElementById('createUpdateForm')
    var movie = {}
    movie.name = form.querySelector('input[name="name"]').value
    movie.genre = form.querySelector('select[name="genre"]').value
    movie.description = form.querySelector('input[name="description"]').value
    movie.id = form.querySelector('input[name="iden"]').value
    console.log(JSON.stringify(movie))
    return movie
}
function getmovieFromForm() {
    var form = document.getElementById('createUpdateForm')
    var movie = {}
    movie.name = form.querySelector('input[name="name"]').value
    movie.genre = form.querySelector('select[name="genre"]').value
    movie.description = form.querySelector('input[name="description"]').value
    //movie.id = form.querySelector('input[name="iden"]').value
    //movie.totalVotes = parseInt(form.querySelector('input[name="totalVotes"]').value,10)
    //console.log(JSON.stringify(movie))
    return movie
}

// AJAX 
host = window.location.origin
// Get all movies
function getAllAjax() {
    $.ajax({
        "url": host+"/movies",
        "method": "GET",
        "data": "",
        "dataType": "JSON",
        "success": function (result) {
            console.log(result);
            for (movie of result) {
                addmovieToTable(movie);
            }
        },
        "error": function (xhr, status, error) {
            console.log("error: " + status + " msg:" + error);
        }
    });
}
// Create a movie 
function createmovieAjax(movie) {
    console.log(JSON.stringify(movie));
    $.ajax({
        "url": host+"/movies",
        "method": "POST",
        "data": JSON.stringify(movie),
        "dataType": "JSON",
        contentType: "application/json; charset=utf-8",
        "success": function (result) {
            console.log(result);
        },
        "error": function (xhr, status, error) {
            console.log("error: " + status + " msg:" + error);
        }
    });
}
// Updates a movie
function updatemovieAjax(movie) {
    console.log(JSON.stringify(movie));
    $.ajax({
        "url": host+"/movies/" + encodeURI(movie.name),
        "method": "PUT",
        "data": JSON.stringify(movie),
        "dataType": "JSON",
        contentType: "application/json; charset=utf-8",
        "success": function (result) {
            console.log(result);
        },
        "error": function (xhr, status, error) {
            console.log("error: " + status + " msg:" + error);
        }
    });
}
// Voting function
function votesAjax(index, numvotes) {
    // Need to parse votes as int as they come in as a string
    parseInt(numvotes)
    var votes = "{\"votes\": " + numvotes + "}"
    $.ajax({
        "url": host+"/votes/" + index,
        "method": "PUT",
        "data": votes,
        "dataType": "JSON",
        contentType: "application/json",
        "success": function (result) {
            console.log(result);
        },
        "error": function (xhr, status, error) {
            console.log("error: " + status + " msg:" + error);
        }
    });
}
// Deletes a movie
function deletemovieAjax(name) {
    console.log(JSON.stringify(movie));
    $.ajax({
        "url": host+"/movies/" + encodeURI(name),
        "method": "DELETE",
        "data": "",
        "dataType": "JSON",
        contentType: "application/json; charset=utf-8",
        "success": function (result) {
            console.log(result);
        },
        "error": function (xhr, status, error) {
            console.log("error: " + status + " msg:" + error);
        }
    });
}
getAllAjax();