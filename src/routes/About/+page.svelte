<script>
  import { fly, fade } from 'svelte/transition';
  import { onMount } from 'svelte';

  const title = "About the Automatic Hostel Bell Project";
  const sections = [
    {
      title: "The Inspiration",
      content: `The inspiration behind designing the automated hostel bell system stems from a deep sense of gratitude and devotion to Swami and the institution that has shaped me in countless ways. Swami’s teachings have always emphasized discipline, selflessness, and service to others, and I wanted to contribute something meaningful that would reflect these values. Having experienced firsthand the structure and harmony that the hostel system provides, I felt a strong urge to give back in a way that could enhance it further. The bell system is not just a technical project for me—it is an offering, a small token of appreciation for the discipline, guidance, and love I have received. Every ring of the bell serves as a reminder of the order and rhythm Swami envisioned for our lives, ensuring that time is honored and moments are well spent. Through this initiative, I hope to integrate technology with purpose, making daily routines smoother while upholding the very principles that Swami instilled in us.`
    },
    {
      title: "The Journey",
      content: `My journey in designing this hostel bell system has been incredibly enriching, filled with learning experiences at every step. What began as an idea soon transformed into an exciting challenge, pushing me to explore various aspects of electronics, programming, and automation. I am deeply grateful to Hursh Gupta, who provided me with the initial guidance, helping me navigate through doubts and refine the logical structure of the system. I am also grateful to the teacher incharge Dr. Sumukh Nandan who gave me a lot of motivation and guidance. Along the way, I relied on open-source internet resources, which played a crucial role in expanding my understanding and offering innovative solutions. Additionally, AI became an essential tool, assisting me in generating, optimizing, and verifying the code, ensuring efficiency and reliability. This project was not just about building a bell system; it was a journey of discovery, collaboration, and growth—one that deepened my appreciation for the power of knowledge and the spirit of learning.
      I would also like to extend my gratitude Sundarmurthy Sir, who provided me with the opportunity to work on this project and offered invaluable support throughout its development. His encouragement and insights were instrumental in bringing this project to fruition.
      `
    },
    
  ];

  let loaded = false;

  onMount(() => {
    loaded = true;
  });
</script>

<svelte:head>
  <title>About - Automatic Hostel Bell</title>
  <meta name="description" content="Learn more about the Automatic Hostel Bell Project" />
</svelte:head>

<section class="about-page" class:loaded>
  <h1 class="title" in:fade={{ duration: 600 }}>{title}</h1>

  {#each sections as section, i}
    <div class="section" in:fade={{ duration: 500, delay: i * 150 }}>
      <h2>{section.title}</h2>
      <p>{section.content}</p>
    </div>
  {/each}

  <div class="contact" in:fade={{ duration: 500 }}>
    <h3>Contact</h3>
    <p>Contact/Quiries/Feedback: <a href="https://puspa-opal.vercel.app/">Puspa Kamal Rai</a></p>
  </div>
</section>

<style>
  body {
    margin: 0;
    padding: 0;
    font-family: 'Inter', sans-serif;
    background: #f4f4f9;
    color: #333;
  }

  .about-page {
    max-width: 800px;
    margin: 40px auto;
    padding: 20px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    opacity: 0;
    transition: opacity 0.5s ease-in-out;
  }

  .about-page.loaded {
    opacity: 1;
  }

  .title {
    text-align: center;
    font-size: 2em;
    margin-bottom: 20px;
    color: #2c3e50;
  }

  .section {
    margin-bottom: 30px;
    padding: 15px;
    background: #f9f9f9;
    border-radius: 8px;
  }

  .section h2 {
    font-size: 1.5em;
    color: #34495e;
    margin-bottom: 10px;
  }

  .section p {
    font-size: 1.1em;
    line-height: 1.6;
    color: #555;
  }

  .contact {
    text-align: center;
    padding-top: 10px;
  }

  .contact a {
    color: #007bff;
    text-decoration: none;
  }

  .contact a:hover {
    text-decoration: underline;
  }
</style>