datapath=../../data

prefix=$1
#echo "de2en prepare data all sizes"
#echo [Preparing test set for EN]
java -ea -Xmx2000m  -cp ../../bin CollectionPreprocessor --rnnlm --text-dir $datapath/rcv-from-binod/test/en --idf $datapath/idfs/idf.en --word-embeddings $prefix.en  --vector-file $prefix.doc.test.en-de.en

#echo [Preparing train set for DE]
java -ea -Xmx2000m  -cp ../../bin CollectionPreprocessor --rnnlm --text-dir $datapath/rcv-from-binod/train/DE1000 --idf $datapath/idfs/idf.de --word-embeddings $prefix.de  --vector-file $prefix.doc.train.en-DE1000.de
