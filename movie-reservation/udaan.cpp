#include <bits/stdc++.h>
#define FAST_IO ios_base::sync_with_stdio(false); cin.tie(NULL)
#define endl "\n"
#define eb   emplace_back
#define ef   emplace_front
#define pb   push_back
#define pf   push_front
#define popb pop_back
#define popf pop_front
#define mp   make_pair
#define f first
#define s second
typedef long long ll;
using namespace std;
//ticket reservation system
class Screen {
	int row, col;
	vector<vector<bool>> seats;
	set<int> aisleSeats;
public:
	Screen(vector<string> line) {
		this->row = stoi(line[2]);
		this->col = stoi(line[3]);
		for (ll i = 4; i < line.size(); i++) {
			aisleSeats.insert(stoi(line[i]));
		}
		vector<vector<bool>> seats(row + 1, vector<bool>(col + 1, false));
		this->seats = seats;
		cout << "Success" << endl;
	}

	void vacant(int r) {
		r;
		for (ll i = 1; i <= col; i++) {
			if (!seats[r][i]) {
				cout << i  << ' ';
			}
		}
		cout << endl;
	}

	void reserve(vector<string>line) {
		int r = stoi(line[2]);
		bool ok = true;
		for (ll i = 3; i < line.size(); i++) {
			if (seats[r][stoi(line[i])]) {
				ok = false;
			}
		}
		if (!ok) {
			cout << "Failure\n";
		}
		else {
			for (ll i = 3; i < line.size(); i++) {
				seats[r][stoi(line[i])] = true;
			}
			cout << "Success\n";
		}
	}

	void suggest(vector<string>line) {
		int r = stoi(line[3]);
		int numSeats = stoi(line[2]);
		int choice = stoi(line[4]);
		int start = choice - numSeats + 1;
		bool ok1 = true;
		bool ok2 = true;
		int end = choice + numSeats - 1;
		if (start<1 or end>col) {
			cout << "None\n";
			return;
		}
		if (start >= 1) {
			for (int i = start; i <= choice; i++) {
				if (aisleSeats.find(i) != aisleSeats.end() and (i > start and i < choice) ) {
					ok1 = false;
					break;

				}
				if (seats[r][i]) {
					ok1 = false;
					break;
				}

			}
		}
		else if (end <= col) {
			for (int i = choice; i <= end ; i++) {
				if (aisleSeats.find(i) != aisleSeats.end() and (i > choice and i < end) ) {
					ok2 = false;
					break;
				}
				if (seats[r][i]) {
					ok2 = false;
					break;
				}

			}
		}
		if (ok1) {
			for (int i = start; i <= choice; i++) {
				cout << i << ' ';
			}
		}
		else if (ok2) {
			for (int i = choice; i <= end ; i++) {
				cout << i << ' ';
			}
		}
		else {
			cout << "None";
		}
		cout << endl;

	}
};

vector<string> words(string str) {
	string word = "";
	vector<string> res;
	for (auto it : str) {
		if (it == ' ') {
			res.push_back(word);
			word = "";
		}
		else {
			word += it;
		}
	}
	res.push_back(word);
	return res;
}

int main()
{
#ifndef ONLINE_JUDGE
	freopen("input.txt", "r", stdin);
	freopen("output.txt", "w", stdout);
#endif
	ll t;
	string str;
	getline(cin, str);
	t = stoi(str);
	map<string, Screen*>mp;
	while (t--) {
		getline(cin, str);
		vector<string> line = words(str);
		string op = line[0];
		if (op == "add-screen") {
			if (mp.find(line[1]) != mp.end()) {
				cout << "Failure\n";
			}
			else
				mp[line[1]] = new Screen(line);
		}
		else if (op == "get-unreserved-seats") {
			//cout << line[2] << ' ';
			if (mp.find(line[1]) == mp.end()) {
				cout << "Failure\n";
			}
			else
				mp[line[1]]->vacant(stoi(line[2]));
		}
		else if (op == "reserve-seat") {
			if (mp.find(line[1]) == mp.end()) {
				cout << "Failure\n";
			}
			else
				mp[line[1]]->reserve(line);
		}
		else if (op == "suggest-contiguous-seats") {
			if (mp.find(line[1]) == mp.end()) {
				cout << "Failure\n";
			}
			else
				mp[line[1]]->suggest(line);

		}
	}
}
