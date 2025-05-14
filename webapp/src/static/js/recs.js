const gatewayBaseUrl =
  document.querySelector('meta[name="api-base-url"]')?.content ||
  "http://localhost:8004";

function renderLoading() {
  const container = document.getElementById("recommendations");
  container.innerHTML = `
    <div class="d-flex justify-content-center w-100 my-4">
      <div class="spinner-border text-secondary" role="status"></div>
    </div>
  `;
}

async function fetchRecommendations() {
  renderLoading();
  try {
    const res = await fetch(`${gatewayBaseUrl}/recs/recs`, {
      method: "GET",
      credentials: "include"
    });
    if (res.status === 401) {
      const err = await res.json();
      // alert(`Not authorized: ${err.error}`);
      return renderMessage("You are not authorized. Login or create an account first");
    }
    const recommendations = await res.json(); // array of { img_id, title_id, original_name }
    renderRecommendations(recommendations);
  } catch (err) {
    console.error(err);
    renderMessage("Error getting recommendations. Try again later.");
  }
}

function renderMessage(text) {
  const container = document.getElementById("recommendations");
  container.innerHTML = `
    <div class="col-12">
      <div class="alert alert-danger text-center w-100" role="alert">${text}</div>
    </div>`;
}

function renderRecommendations(items) {
  const container = document.getElementById("recommendations");
  container.innerHTML = "";

  if (items.length === 0) {
    return renderMessage("No recommendations found");
  }

  items.forEach(item => {
    const { img_id, title_id, original_name } = item;

    const col = document.createElement("div");
    col.className = "col-sm-6 col-md-4 col-lg-3";

    const card = document.createElement("div");
    card.className = "card movie-card h-100 shadow-sm";

    const img = document.createElement("img");
    img.src = `/static/images/${img_id}.jpg`;
    img.alt = original_name;
    img.className = "card-img-top";

    // wrap poster in a link to the IMDB page
    const link = document.createElement("a");
    link.href = `http://imdb.com/title/${title_id}`;
    link.target = "_blank";
    link.append(img);

    const body = document.createElement("div");
    body.className = "card-body d-flex flex-column";

    const title = document.createElement("h5");
    title.className = "card-title";
    title.innerText = original_name;

    const btnLike = document.createElement("button");
    btnLike.className = "btn btn-outline-secondary flex-fill";
    btnLike.innerText = "👍";
    btnLike.onclick = () => {
      sendInteraction(img_id, 'like');
      btnLike.classList.remove('btn-outline-secondary');
      btnLike.classList.add('btn-success');      // keep it filled/colored
      btnLike.disabled = true;                  // prevent double‑voting
      btnDislike.disabled = true;
    };

    const btnDislike = document.createElement("button");
    btnDislike.className = "btn btn-outline-secondary flex-fill";
    btnDislike.innerText = "👎";
    btnDislike.onclick = () => {
      sendInteraction(img_id, 'dislike');
      btnDislike.classList.remove('btn-outline-secondary');
      btnDislike.classList.add('btn-danger');   // colored state
      btnLike.disabled = true;                  // prevent double‑voting
      btnDislike.disabled = true;
    };

    const btnContainer = document.createElement("div");
    btnContainer.className = "d-flex w-100 mt-auto gap-2";
    btnContainer.append(btnLike, btnDislike);

    body.append(title, btnContainer);
    card.append(link, body);
    col.append(card);
    container.append(col);
  });
}

async function sendInteraction(itemId, action) {
  try {
    const res = await fetch(`${gatewayBaseUrl}/interact/interact`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ item_id: itemId, action: action }),
    });

    if (res.status === 409) {
      alert("You have already rated this movie/series");
      return;
    }

    if (!res.ok) {
      const errorData = await res.json();
      alert(errorData.detail ?? "Error sending interaction");
      return;
    }

    // Optionally handle successful interaction here
  } catch (err) {
    console.error("Error sending interaction", err);
    alert("Error sending interaction");
  }
}

// New function to handle payment and fetch recommendations
async function handleGetRecommendations() {
  try {
    const paymentRes = await fetch(`${gatewayBaseUrl}/profile/change_balance`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ balance_change: -100.0 })
    });

    if (paymentRes.status === 401) {
      return renderMessage("You are not authorized. Login or create an account first");
    }

    if (!paymentRes.ok) {
      const errorData = await paymentRes.json();
      return renderMessage(errorData.detail ?? 'Payment failed. Please ensure sufficient balance.');
    }

    fetchRecommendations();
  } catch (error) {
    console.error("Error processing payment", error);
    renderMessage("Error processing payment. Try again later.");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("recommendations");
  container.innerHTML = '';

  const payButton = document.createElement("button");
  payButton.id = "get-recs-button";
  payButton.className = "btn btn-secondary d-block mx-auto mb-3";
  payButton.innerText = "Recommend me!";
  payButton.onclick = handleGetRecommendations;
  container.parentNode.insertBefore(payButton, container);
});