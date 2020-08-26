const BASE_URL = "http://127.0.0.1:5000/api"

function generateCupcakeHTML(cupcake){
    return `
    <div class="col-sm-6 col-xl-4 my-1">
      <div class="card">
        <div class="img-thumbnail">
          ${cupcake.flavor} flavor
        </div>
        <img src="${cupcake.image}" class="card-img-top" alt="${cupcake.flavor} cupcake">
        <div class="card-body">
          <div class="card-text">
            <p> Size: ${cupcake.size}</p>
            <p> Rating: ${cupcake.rating}</p>
          </div>
        </div>
        <button class="btn btn-small btn-danger delete-button" id = "${cupcake.id}">Delete</button>
      </div>
    </div>
    `;
}

async function showCupcakes(){
    const response = await axios.get(
        `${BASE_URL}/cupcakes`
    );

    for (let cupcakeData of response.data.cupcakes){
        let newCupcake = $(generateCupcakeHTML(cupcakeData));
        $("#cupcakes-list").append(newCupcake)
    }
}


$("#add-cupcake-form").on("submit", async function (evt){

    evt.preventDefault();

    const response = await axios.post(
        `${BASE_URL}/cupcakes`,
        {
            "flavor" : $("#flavor").val(),
            "rating" : $("#rating").val(),
            "size" : $("#size").val(),
            "image" : $("#image").val()
 
        }
    );

    let newCupcake = $(generateCupcakeHTML(response.data.cupcake));
    $("#cupcakes-list").prepend(newCupcake);
    $("#add-cupcake-form").trigger("reset")

});

$("#cupcakes-list").on("click", ".delete-button", async function(evt){
    evt.preventDefault();

    let cupcakeID = $(evt.target).attr("id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeID}`);

    $(this).parent().remove()

});


$(showCupcakes);
