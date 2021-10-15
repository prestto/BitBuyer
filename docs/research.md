# Research

## Front

- [Folder structure](https://stackoverflow.com/questions/48799272/angular-folders-files-structure-for-a-simple-app-style-guide)
- [meduim article for folder structure](https://michelestieven.medium.com/organizing-angular-applications-f0510761d65a)

## PK out of sequence

The serial pk of the coin_prices table somehow got out of sequence.  it seems a manual reset is the recommended solution:

```sql
SELECT setval('coin_prices_id_seq', (SELECT MAX(id) FROM coin_prices)+1);
```

## Organizing Kustomize files

- [structuring dev & prod files](https://www.digitalocean.com/community/tutorials/how-to-manage-your-kubernetes-configurations-with-kustomize)