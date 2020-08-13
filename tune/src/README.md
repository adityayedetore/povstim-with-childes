```
python main.py --data $data --nlayers $nlayers --nhid $nhid --emsize $nhid --lr $lr --batch_size $batch_size --dropout $dropout --seed $seed --epochs $epochs --save $save --log $log --cuda

python main.py --data tune-data --epochs 4 --save "model.pt~tuned" --log tune-log.txt 
```
