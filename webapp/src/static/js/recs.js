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
    const { item_ids = [] } = await res.json();
    renderRecommendations(item_ids);
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

function renderRecommendations(itemIds) {
  const container = document.getElementById("recommendations");
  container.innerHTML = "";

  if (itemIds.length === 0) {
    return renderMessage("No recommendations found");
  }

  itemIds.forEach(id => {
    const col = document.createElement("div");
    col.className = "col-sm-6 col-md-4 col-lg-3";

    const card = document.createElement("div");
    card.className = "card movie-card h-100 shadow-sm";

    const img = document.createElement("img");
    img.src = `/static/images/${id}.jpg`;
    img.alt = `Movie ${id}`;
    img.className = "card-img-top";

    const body = document.createElement("div");
    body.className = "card-body d-flex flex-column";

    const title = document.createElement("h5");
    title.className = "card-title";
    title.innerText = `Movie №${id}`;

    const btnLike = document.createElement("button");
    btnLike.className = "btn btn-outline-secondary flex-fill";
    btnLike.innerText = "👍";
    btnLike.onclick = () => sendInteraction(id, 'like');

    const btnDislike = document.createElement("button");
    btnDislike.className = "btn btn-outline-secondary flex-fill";
    btnDislike.innerText = "👎";
    btnDislike.onclick = () => sendInteraction(id, 'dislike');

    const btnContainer = document.createElement("div");
    btnContainer.className = "d-flex w-100 mt-auto gap-2";
    btnContainer.append(btnLike, btnDislike);

    body.append(title, btnContainer);
    card.append(img, body);
    col.append(card);
    container.append(col);
  });
}

async function sendInteraction(itemId, action) {
  try {
    await fetch(`${gatewayBaseUrl}/interact/interact`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ item_id: itemId, action: action }),
    });
  } catch (err) {
    console.error("Error sending interaction", err);
    alert("Error sending interaction");
  }
}

// New function to handle payment and fetch recommendations
async function handleGetRecommendations() {
  try {
    const paymentRes = await fetch(`${gatewayBaseUrl}/user/change_balance`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ balance_change: -100.0 })
    });
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