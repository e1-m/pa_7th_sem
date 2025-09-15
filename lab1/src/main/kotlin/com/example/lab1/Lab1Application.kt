package com.example.lab1

import org.springframework.boot.CommandLineRunner
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.stereotype.Component

@SpringBootApplication
class Lab1Application

fun main(args: Array<String>) {
    runApplication<Lab1Application>(*args)
}

@Component
class ArrayMaxRunner : CommandLineRunner {
    override fun run(vararg args: String?) {
        println("Enter numbers separated by spaces:")

        val input = readlnOrNull() ?: ""
        val numbers = input.split(" ")
            .mapNotNull { it.toIntOrNull() }

        if (numbers.isEmpty()) {
            println("No valid numbers provided.")
        } else {
            val maxNumber = numbers.maxOrNull()
            println("The maximum number is: $maxNumber")
        }
    }
}
