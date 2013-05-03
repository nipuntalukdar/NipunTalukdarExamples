; Below function checks if an object is memember of a list
; call it as shown below 
; (ourmember '1 '(4 1 2 3))

(defun ourmember (x lst)
	( and 
		(consp lst )
		(if (equal x (car lst))
			lst
			(ourmember x (cdr lst))
		)
	)
)


; Below function simulates built-in adjoin function
; call it as shown below
; (ouradjoin  '1  '(2 3 4))

(defun ouradjoin(x lst)
	(and
		(consp lst)
		( if (ourmember x lst)
			lst
			(cons x lst)
		) 
	)
)

; Below function simulates union of two lists. This is not an 
; efficient implementation, but demonstrates the operation
; call it as shown below
; (ourunion '(1 2) '(1 3 4))

(defun ourunion (lst1 lst2)

	( if (null lst2)
		( if (consp lst1)
			lst1
			nil
		)
		(ourunion (ouradjoin (car lst2) lst1) (cdr lst2))
	)
)




; Below function checks if a list is a palindrome
; 

( defun palindrome(lst)
	( if (null lst)
		nil
		(let ((len (length lst)))
			( and 
				(evenp len)
				(let ((mid (/ len 2) ))
					(equal
						(subseq lst 0 mid)
						(reverse (subseq lst mid)) 
					)
				)
			)
		)
	)
)

; Below is a function to reverse a list
; it should be called like (ourreverse '(1 2 3 4))

(defun ourreverse (lst)
	(if (consp lst)
		( let ((ace nil ))
			( dolist (elt lst)
				(push elt ace)
			)
			ace
		)
		nil
	)	
)

; Below is a function that checks if a list is proper
; (properlist  '(1 2 3))

(defun properlist(lst)
	(or
		(null lst)
		( and
			( consp lst)
			( properlist (cdr lst))
		)

	)
)


; Below function checks if a key is an associated list'
; 

(defun keyin(key lst)
	(and 
		(consp lst)
		(let ((x (car lst)))
		 	( if (eql key (car x))
		 		x
		 		(keyin key (cdr lst))
		 	)
		) 
	)
)

