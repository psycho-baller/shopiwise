package handler

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"

	"github.com/sashabaranov/go-openai"
)

type RequestBody struct {
	ProductTitle string `json:"productTitle"`
	UserInfo     string `json:"userInfo"`
}

func Intentions(w http.ResponseWriter, r *http.Request) {
	// Check if the request method is POST
	if r.Method != http.MethodPost {
	http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	return
	}
	// Parse the request body
	var requestBody RequestBody
	if err := json.NewDecoder(r.Body).Decode(&requestBody); err != nil {
		http.Error(w, "Bad request", http.StatusBadRequest)
		return
	}
	
	userInfo := requestBody.UserInfo
	productTitle := requestBody.ProductTitle
	formatResponse := `The output should be formatted as a JSON instance that conforms to the JSON schema below.\n\nAs an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}\nthe object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.\n\nHere is the output schema:\n~~~\n{"properties": {"intentions": {"title": "Intentions", "description": "List of potential unrecognized intentions", "type": "array", "items": {"$ref": "#/definitions/Intention"}}}, "required": ["intentions"], "definitions": {"Intention": {"title": "Intention", "type": "object", "properties": {"title": {"title": "Title", "description": "Title of the potential unrecognized intention", "type": "string"}, "description": {"title": "Description", "description": "The description of the potential unrecognized intention", "type": "string"}}, "required": ["title", "description"]}}}\n~~~'}`
	client := openai.NewClient(os.Getenv("OPENAI_API_KEY"))
	resp, err := client.CreateChatCompletion(
		context.Background(),
		openai.ChatCompletionRequest{
			Model:     openai.GPT3Dot5Turbo,
			// MaxTokens: 5,
			Messages: []openai.ChatCompletionMessage{
				{
					Role:    openai.ChatMessageRoleUser,
					Content: fmt.Sprintf("%s. I found this amazon product named \"%s\" Could you warn me of the potential unrecognized intentions that might be motivating me to buy this item? I wanna ensure that I'm not going to regret buying this item in a few weeks from now.\n %s", userInfo, productTitle, formatResponse),
				},
			},
		},
	)
	if err != nil {
		fmt.Printf("Completion error: %v\n", err)
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(resp.Choices[0].Message.Content))
}
