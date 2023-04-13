Required packages: streamlit, pandas, numpy

To run the code:

```
git clone --branch master git@github.com:Xiyuan0315/PPIs-visualization.git
cd PPIs-visualization/Bin
streamlit run app.py
```

### Project overview

The project aims to develop a high performance website for visualizing and filtering annonated PPIS from Baker’s lab on user’s demand.

### Workflow

1. Preprocessing the table data with re and pandas to format the text, downcast datatype and work with missing data(replace ‘na’ to np.NaN to make datatype consistent)
2. Display 1505 pairs of yeast PPIs in the body part, and add dynamic filters on it. Notably that we take different actions on continous data and discrete: double end slider for continous data and regex reseaching/multi-selection for discrete data.
3. Add global searching funcion in sidebar to search on all annotation columns.
4. Provide two mode for multi-keywords with check box: intersection or union
5. Implement multi-pages for different function(filter, find homologous genes, explore protein location and get genes in given pathways)

### Disccusion

1. path management: setup.py
2. variable passing to seperate pages: serialize filtered data as pickle and load again in next page
3. Make two different filter space works together without duplicated computing: use cache decorater that re-defined in streamlit

Web preview:
<img width="958" alt="image" https://github.com/Xiyuan0315/PPIs-visualization/blob/master/example/filter.png>
<img width="958" alt="image" https://github.com/Xiyuan0315/PPIs-visualization/blob/master/example/homo.png>
<img width="958" alt="image" https://github.com/Xiyuan0315/PPIs-visualization/blob/master/example/pathway.png>
