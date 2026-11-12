// The door only knocks. The guards decide on the server.
const $ = (id) => document.getElementById(id);

function setLocks(n) {
  document.querySelectorAll("#locks .lock").forEach((el, i) => {
    el.classList.toggle("open", i < n);
  });
}

$("knock").addEventListener("click", async () => {
  const btn = $("knock");
  btn.disabled = true;
  try {
    const res = await fetch("/api/knock", { method: "POST" });
    const data = await res.json();
    setLocks(data.locks_open || 0);
    $("msg").textContent = data.message || "";
    if (data.ok && data.flag) {
      $("door").hidden = true;
      $("win").hidden = false;
      $("flag").textContent = data.flag;
    }
  } catch (e) {
    $("msg").textContent = "The door shimmers and goes quiet. Try again.";
  } finally {
    btn.disabled = false;
  }
});
