<?php

namespace App\Security;

use App\Entity\User;
use Firebase\JWT\JWT;
use Psr\Log\LoggerInterface;
use Symfony\Contracts\HttpClient\HttpClientInterface;
class UserMediator {
    function __construct(
        private HttpClientInterface $client,
    ) {
    }

    public function sync(String $user, array $roles): User
    {
        $payload = [
            'user_id' => $user,
            'role' => $roles,
            'iat' => time(),
            'exp' => time() + 3600
        ];

        $jwt = JWT::encode($payload, $_ENV['JWT_SECRET'], 'HS256');
        json_encode([
            'status' => 'success',
            'token' => $jwt
        ]);
        try {
            $apiUrl = $_ENV['API_URL'] ?? 'http://127.0.0.1:8001';
            $response = $this->client->request('POST', "{$apiUrl}/api/users/sync", [
                'auth_bearer' => $jwt,
                'json' => [
                    'username' => $user,
                    'roles' => $roles,
                ],
                'timeout' => 2.0,
            ]);
            $data = $response->toArray();
            return new User($data['username'], $data['roles']);
        } catch (\Throwable $e) {
            return new User($user, $roles);
        }
    }

}