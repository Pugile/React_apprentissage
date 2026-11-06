<?php

namespace App\Security;

use App\Entity\User;
use Psr\Log\LoggerInterface;
use Symfony\Contracts\HttpClient\HttpClientInterface;
class UserMediator {
    function __construct(
        private HttpClientInterface $client,
    ) {
    }

    public function sync(String $user, array $roles) {
        try {
            $apiUrl = $_ENV['API_URL'] ?? 'http://127.0.0.1:8001';
            $response = $this->client->request('POST', "{$apiUrl}/api/users/sync", [
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