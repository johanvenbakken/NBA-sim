function velgspiller() {
    const element = document.getElementById("draft_headerskrift");
    if (element.innerHTML === "DRAFT - spiller1, velg spiller") {
        element.innerHTML = "DRAFT - spiller2, velg spiller";
    } else {
        element.innerHTML = "DRAFT - spiller1, velg spiller";
    }
}

const paragraphs = document.querySelectorAll('.draft_spilleretekst');

let counter = 0;
let penger_laga = 15;
let penger_lagb = 15;

function changeColorOnClick(event) {
  const clickedElement = event.target; 

  if (clickedElement.classList.contains('clicked')) {
      return; 
  }
  // Check if the clicked element is a <p> tag inside a div with class "draft_rad2"
  let isInDraftRad2 = clickedElement.closest('div.draft_rad2') !== null;
  
  if (isInDraftRad2) {
    if (counter % 2 == 0){
      penger_laga -= 5
      document.getElementById("pengesum_lagA").innerHTML = penger_laga + "$";
    } else{
      penger_lagb -= 5
      document.getElementById("pengesum_lagB").innerHTML = penger_lagb + "$";
    }
  };
  let isInDraftRad3 = clickedElement.closest('div.draft_rad3') !== null;
  
  if (isInDraftRad3) {
    if (counter % 2 == 0){
      penger_laga -= 4
      document.getElementById("pengesum_lagA").innerHTML = penger_laga + "$";
    } else{
      penger_lagb -= 4
      document.getElementById("pengesum_lagB").innerHTML = penger_lagb + "$";
    }
  };
  let isInDraftRad4 = clickedElement.closest('div.draft_rad4') !== null;
  
  if (isInDraftRad4) {
    if (counter % 2 == 0){
      penger_laga -= 3
      document.getElementById("pengesum_lagA").innerHTML = penger_laga + "$";
    } else{
      penger_lagb -= 3
      document.getElementById("pengesum_lagB").innerHTML = penger_lagb + "$";
    }
  };
  let isInDraftRad5 = clickedElement.closest('div.draft_rad5') !== null;
  
  if (isInDraftRad5) {
    if (counter % 2 == 0){
      penger_laga -= 2
      document.getElementById("pengesum_lagA").innerHTML = penger_laga + "$";
    } else{
      penger_lagb -= 2
      document.getElementById("pengesum_lagB").innerHTML = penger_lagb + "$";
    }
  };
  let isInDraftRad6 = clickedElement.closest('div.draft_rad6') !== null;
  
  if (isInDraftRad6) {
    if (counter % 2 == 0){
      penger_laga -= 1
      document.getElementById("pengesum_lagA").innerHTML = penger_laga + "$";
    } else{
      penger_lagb -= 1
      document.getElementById("pengesum_lagB").innerHTML = penger_lagb + "$";
    }
  };

  
  if (counter % 2 === 0) {
    clickedElement.style.color = 'blue';
  } else {
    clickedElement.style.color = 'red';
  } 

  clickedElement.classList.add('clicked');

  counter++;


    if (counter === 1) {
        document.getElementById("lagA_spiller1").innerHTML = clickedElement.textContent;
    } else if (counter === 2) {
        document.getElementById("lagB_spiller1").innerHTML = clickedElement.textContent;
    } else if (counter === 3) {
        document.getElementById("lagA_spiller2").innerHTML = clickedElement.textContent;
    } else if (counter === 4) {
        document.getElementById("lagB_spiller2").innerHTML = clickedElement.textContent;
    } else if (counter === 5) {
        document.getElementById("lagA_spiller3").innerHTML = clickedElement.textContent;
    } else if (counter === 6) {
        document.getElementById("lagB_spiller3").innerHTML = clickedElement.textContent;
    } else if (counter === 7) {
        document.getElementById("lagA_spiller4").innerHTML = clickedElement.textContent;
    } else if (counter === 8) {
        document.getElementById("lagB_spiller4").innerHTML = clickedElement.textContent;
    } else if (counter === 9) {
        document.getElementById("lagA_spiller5").innerHTML = clickedElement.textContent;
    } else if (counter === 10) {
        document.getElementById("lagB_spiller5").innerHTML = clickedElement.textContent;
    }
}

paragraphs.forEach(function(p) {
    p.addEventListener('click', changeColorOnClick);
});

const basketballPlayers = {
  PG: {
    $5: [
      { name: "M Johnson", attacking: 98, defensive: 85 },
      { name: "S Curry", attacking: 100, defensive: 80 }
    ],
    $4: [
      { name: "C Paul", attacking: 92, defensive: 88 },
      { name: "R Rondo", attacking: 85, defensive: 75 }
    ],
    $3: [
      { name: "R Westbrook", attacking: 92, defensive: 85 },
      { name: "D Rose", attacking: 88, defensive: 70 }
    ],
    $2: [
      { name: "I Thomas", attacking: 88, defensive: 70 },
      { name: "A Iverson", attacking: 91, defensive: 70 }
    ],
    $1: [
      { name: "D Johnson", attacking: 87, defensive: 70 },
      { name: "R Miyagi", attacking: 82, defensive: 60 }
    ]
  },
  SG: {
    $5: [
      { name: "M Jordan", attacking: 100, defensive: 98 },
      { name: "K Bryant", attacking: 98, defensive: 93 }
    ],
    $4: [
      { name: "D Wade", attacking: 92, defensive: 85 },
      { name: "R Allen", attacking: 93, defensive: 60 }
    ],
    $3: [
      { name: "J Harden", attacking: 95, defensive: 65 },
      { name: "K Thompson", attacking: 88, defensive: 75 }
    ],
    $2: [
      { name: "D Booker", attacking: 93, defensive: 75 },
      { name: "J Holiday", attacking: 87, defensive: 88 }
    ],
    $1: [
      { name: "D Mitchell", attacking: 92, defensive: 78 },
      { name: "Z LaVine", attacking: 85, defensive: 55 }
    ]
  },
  SF: {
    $5: [
      { name: "L James", attacking: 100, defensive: 90 },
      { name: "L Bird", attacking: 98, defensive: 85 }
    ],
    $4: [
      { name: "K Durant", attacking: 98, defensive: 78 },
      { name: "K Leonard", attacking: 92, defensive: 90 }
    ],
    $3: [
      { name: "S Pippen", attacking: 88, defensive: 85 },
      { name: "P George", attacking: 90, defensive: 80 }
    ],
    $2: [
      { name: "J Erving", attacking: 92, defensive: 70 },
      { name: "J Worthy", attacking: 88, defensive: 68 }
    ],
    $1: [
      { name: "V Carter", attacking: 80, defensive: 55 },
      { name: "D Wilkins", attacking: 77, defensive: 60 }
    ]
  },
  PF: {
    $5: [
      { name: "T Duncan", attacking: 94, defensive: 97 },
      { name: "K Garnett", attacking: 90, defensive: 88 }
    ],
    $4: [
      { name: "D Nowitzki", attacking: 95, defensive: 60 },
      { name: "D Rodman", attacking: 70, defensive: 100 }
    ],
    $3: [
      { name: "K Malone", attacking: 94, defensive: 75 },
      { name: "C Webber", attacking: 88, defensive: 70 }
    ],
    $2: [
      { name: "J Jackson Jr.", attacking: 85, defensive: 80 },
      { name: "B Adebayo", attacking: 86, defensive: 85 }
    ],
    $1: [
      { name: "P Siakam", attacking: 75, defensive: 60 },
      { name: "Z Randolph", attacking: 80, defensive: 72 }
    ]
  },
  C: {
    $5: [
      { name: "K Abdul-Jabbar", attacking: 100, defensive: 92 },
      { name: "H Olajuwon", attacking: 92, defensive: 95 }
    ],
    $4: [
      { name: "Shaq O'Neal", attacking: 97, defensive: 80 },
      { name: "W Chamberlain", attacking: 100, defensive: 85 }
    ],
    $3: [
      { name: "B Russell", attacking: 80, defensive: 100 },
      { name: "P Ewing", attacking: 88, defensive: 80 }
    ],
    $2: [
      { name: "D Robinson", attacking: 90, defensive: 85 },
      { name: "A Mourning", attacking: 85, defensive: 88 }
    ],
    $1: [
      { name: "D Howard", attacking: 70, defensive: 75 },
      { name: "J Embiid", attacking: 92, defensive: 85 }
    ]
  }
};

window.onload = function () {
  function updatePlayer(position, rank) {
      const players = basketballPlayers[position]["$" + rank]; // Tilgang til spillerlisten
      const randomIndex = Math.floor(Math.random() * players.length); // Tilfeldig indeks
      const randomPlayer = players[randomIndex]; // Hent tilfeldig spiller
      document.getElementById(position.toLowerCase() + (6-rank)).innerHTML = randomPlayer.name; // Oppdater HTML
  }

  const positions = ["PG", "SG", "SF", "PF", "C"];
  const ranks = [1, 2, 3, 4, 5];

  positions.forEach(position => {
      ranks.forEach(rank => {
          updatePlayer(position, rank);
      });
  });
};


document.getElementById("submitBtn").addEventListener('click', function(){

  const lagA = {
    spiller1: document.getElementById("lagA_spiller1").textContent,
    spiller2: document.getElementById("lagA_spiller2").textContent,
    spiller3: document.getElementById("lagA_spiller3").textContent,
    spiller4: document.getElementById("lagA_spiller4").textContent,
    spiller5: document.getElementById("lagA_spiller5").textContent
  }

  const lagB = {
    spiller1: document.getElementById("lagB_spiller1").textContent,
    spiller2: document.getElementById("lagB_spiller2").textContent,
    spiller3: document.getElementById("lagB_spiller3").textContent,
    spiller4: document.getElementById("lagB_spiller4").textContent,
    spiller5: document.getElementById("lagB_spiller5").textContent
  }

  fetch('/submit', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json'
      },
      body: JSON.stringify({ lagA, lagB})
  })
  .then(response => response.json())
  .then(data => {
    console.log("sucess:", data);

    window.location.href = "/simulering";
  })
  .catch((error) => {
    console.error("error:", error)
  })

})
