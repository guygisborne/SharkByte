# install LDAP extension
def ldap_login(username, password):
	import ldap
	LDAP_SERVER = 'ldap://172.16.0.85'
	LDAP_DN = 'ou=ZimbraUsers,dc=escapemg,dc=com'
	con = ldap.initialize(LDAP_SERVER)
	result = con.search_s(LDAP_DN, ldap.SCOPE_SUBTREE, '(uid=%s)' % username, ['cn', 'mail'])

	if not result:
		return False

	user_dn = result[0][0]
	user_name = result[0][1]['cn'][0]

	try:
		con.bind_s(user_dn, password)
		return True
	except ldap.INVALID_CREDENTIALS:
		return False


if __name__ == '__main__':
	print 'test'
	print ldap_login('thomas', 'cheese')
	print ldap_login('abraham.alrajhi', 'somethng')
