<p align="center">
  <a>
    <img src="UP logo.png" alt="Logo" height="100">
  </a>

<h2 align="center">Fakulteti i Inxhinierisë Elektrike dhe Kompjuterike</h2>
<h3 align="center">Lënda: Dizajni dhe Analiza e Algoritmeve</h3>
<h2 align="center">Projekti: Recommender System with Collaborative Filtering</h2>
<p align="left">Profesori: Avni Rexhepi</p>
<p align="left">Asistenti: Adrian Ymeri</p>

<p align="left">Studentët: Jon Kuçi, Kaltrina Krasniqi, Erza Gashi, Edon Gashi</p><br><br>

</p><br>

## Përmbledhje e Projektit

This program is a recommendation system using collaborative filtering. The program takes as input 3 JSON files, which contain a list of users, a list of books, and a dataset describing the ratings users give to books. The program can determine which books a specific user might like the most, based on the ratings they have given to other similar books. To achieve the most accurate results, calculations are performed using two methods: `Cosine Similarity` and `Pearson Similarity`, and their average is computed.
<br><br>

 <br><br>
## Përdorimi
Menyra e perdorimit
To execute, simply run the `main.py` file, which contains the mergeItemAndUserBased method within the MergingItemAndUserBased class. This method accepts 4 inputs:

 - `userId`: the ID of the user for whom you want to predict which books they might like.
 - `data`: the input dataset.
 - `automatic`: if set to true, it automatically adjusts the weight of the result calculated with cosine similarity relative to the result from Pearson similarity (depending on the number of ratings users have given for the books). If set to false, an additional value (the alpha coefficient) must be provided, which indicates the level of importance cosine similarity will have in the final result.

After this method is executed, a list of books will be displayed that the user with the specified ID might like based on their previous preferences. The list is sorted by similarity to the liked books and the ratings those books have received.
<p align="center"> Gif 1
<a>
    <img src="" alt="Logo" height="430" align="center">
  </a>
  </p>
<br><br><br>

- P2
 
<p align="center">Gif 2
<a>
    <img src="" alt="Logo" height="350" align="center">
  </a>
</p>

<br><br><br>



<br><br><br>


<br><br>
   <a href="#top">Kthehu në fillim ↑</a>
