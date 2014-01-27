-module(primecheck) .
-export([is_prime/1]).
% You should call it as shown below 
% primecheck:is_prime(23) etc.
%
is_prime(N) when N < 0 ->
    false;
is_prime(N) -> 
    case N of
        1 -> false;
        2 -> true;
        3 -> true;
        0 -> false;
        _ -> is_prime_second(N, 2, math:sqrt(N)) 
    end.
is_prime_second(_, M, L) when  M > L ->
    true;
is_prime_second(N, M, _) when N rem M == 0 ->
    false;
is_prime_second(N, M, L) -> is_prime_second(N, M + 1, L).

