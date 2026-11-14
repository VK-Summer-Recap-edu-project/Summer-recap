## Данные
Для обучения нейросети используется датасет
[EMOTIC](https://github.com/rkosti/emotic) (PAMI-версия).
Датасет не входит в репозиторий: доступ выдаётся по запросу авторам.
После получения распакуйте его в `data/emotic/`
(папки `ade20k`, `emodb_small`, `framesdb`, `mscoco` + `Annotations.mat`). Нейросеть обучалась на данных из `mscoco` и `ade20k`

Аннотации конвертируются скриптом из [Tandon-A/emotic](https://github.com/Tandon-A/emotic).
