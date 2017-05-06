{ Test println } test set

	{ 
	f set e set b set s set
	b get s get set
	
		{
		s get get e get <=
			{
			f get exec
			s get get 1 + s get set
			h get exec
			}
			{ } 
		if
		}
	h set
	h get exec
	}
for set

	{
	n set
	i 1 n get
		{
		tail
		}
	for get exec
	head
	}
getitem set

	{
	v set
	1 
	v get
	
		{	
		duplicate
		v set
		*
		v get
		1
		-
		duplicate
		1
		>
			{
			h get exec
			}
			{
			}
		if
		}
	h set
	h get exec
	
	throw
	}
factorial set

vars export
