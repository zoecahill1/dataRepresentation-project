$(document).ready(function () {
    let apikey = "c460f163";
    // Search function
    function search() {
        // Grab the search term value from input field
        let searchTerm = $('#search').val().toLowerCase(),
            // Set empty HTML value for printing to page after getting search results
            movieHTML = "";
        $.ajax({
            url: 'http://www.omdbapi.com/?apikey=' + apikey + '&s=' + searchTerm,
            method: 'GET',
            dataType: 'json',
            success: function (data) { // If search is successful, create HTMl with list items of movies
                // If search is successful, create HTML with list items of movies
                if (data.Response === "True") {
                    $.each(data.Search, function (i, movie) {
                        movieHTML += '<li id="' + movie.imdbID + '"><div>';
                        // If poster is available, display it
                        if (movie.Poster != "N/A") {
                            movieHTML += '<a href="#" data-toggle="modal" data-target="#' + movie.imdbID + '"><img src="' + movie.Poster + '"></a>';
                            // If not then 
                        } else {
                            movieHTML += "<i>crop_original</i>";
                        }
                        movieHTML += '</div>';
                        movieHTML += '<span>' + movie.Title + '</span>';
                    });
                    // If no movies are found
                } else if (data.Response === "False") {
                    movieHTML += '<li><i>help_outline</i>No movies found that match: ' + searchTerm;
                    $('.movie-list').html(movieHTML);
                }
                // Print the HTML with list of movies to the page
                $('.movie-list').html(movieHTML);

            },
        });
    }


    $('#movies').on('click', "li", function (e) {

        //Prevents the bootstrap modal from bubbling the add '.in' class to the target click
        //https://stackoverflow.com/questions/17883692/how-to-set-time-delay-in-javascript
        e.stopPropagation();
        let movieModal = "",
            movieId = $(this).attr('id');

        $.ajax({
            url: 'http://www.omdbapi.com/?apikey=' + apikey + '&i=' + movieId + '&plot=full',
            method: 'GET',
            dataType: 'json',
            success: function (data) {
                movieModal += '<div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button><h4 class="modal-title">' + data.Title + ' (' + data.Year + ')' + '</h4></div>';
                movieModal += '<div class="modal-body">' + '<img src="' + data.Poster + '"><br><br>IMDB Rating: ' + data.imdbRating + '<br><br>Plot Synopsis:<br>' + data.Plot + '</div>';
                movieModal += '<div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal">Close</button><a href="http://www.imdb.com/title/' + data.imdbID + '" target="_blank"><button type="button" class="btn btn-primary">Link to IMDB</button></a></div></div>';
                $('.modal-dialog').html(movieModal); // Update the clicked modal
                $('#posterModal').modal('show');
            }
        });


    });
    //https://stackoverflow.com/questions/17883692/how-to-set-time-delay-in-javascript
    let delay = (function () {
        let timer = 0;
        return function (callback, ms) {
            clearTimeout(timer);
            timer = setTimeout(callback, ms);
        };
    })();
    //Keyup Function
    $('input').keyup(function () {
        delay(function () {
            search();
        }, 500);
    });
});
