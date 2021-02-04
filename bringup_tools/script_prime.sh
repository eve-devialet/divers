#/bin/sh
if [ $1 -eq 0 ]; then
	prime=866121769378709
elif [ $1 -eq 1 ]; then
	prime=689917708893977
elif [ $1 -eq 2 ]; then
	prime=939952478980861
elif [ $1 -eq 3 ]; then
	prime=587336789917721
else
	prime=223232789711417
fi

#function is_prime(){
is_prime(){
    if [ $1 -eq 2 ] || [ $1 -eq 3 ]; then
        return 1  # prime
    fi
    if [ $(($1 % 2)) -eq 0 ] || [ $(($1 % 3)) -eq 0 ]; then
        return 0  # not a prime
    fi
    i=5; w=2
    while [ $((i * i)) -le $1 ]; do
        if [ $(($1 % i)) -eq 0 ]; then
            return 0  # not a prime
        fi
        i=$((i + w))
        w=$((6 - w))
    done
    return 1  # prime
}

is_prime $prime
if [ $? -eq 0 ]; then
  echo "$prime is not a prime"
else
  echo "$prime is a prime"
fi

